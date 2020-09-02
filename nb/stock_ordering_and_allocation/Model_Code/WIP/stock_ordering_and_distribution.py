#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import random as r
import math
import os
from datetime import timedelta

import matplotlib.pyplot as plot

from pyomo.environ import *
from pyomo.opt import SolverFactory
from gurobipy import GRB


# In[2]:


#id directories
data_dir = '/Users/chelseagreene/ws/github/ws.restart/src/user/chelsea/stock_ordering_and_allocation/Input_Data/Seattle/'
#results_dir = '/Users/chelseagreene/Desktop/Academic/PhD/ResearchAssistanship/Projects/RestartPartners/Results/Seattle'


# In[3]:


max_adj = .3
min_adj = .1
scenarios = ['min', 'mean', 'max']


# In[4]:


#change wd to input data directory
os.chdir(data_dir)

#read data
demand_sources_df = pd.read_excel('Model_Input_Seattle_Example.xlsx', sheet_name ='Demand Sources')
items_df = pd.read_excel('Model_Input_Seattle_Example.xlsx', sheet_name ='Items')
burn_rates_df = pd.read_excel('Model_Input_Seattle_Example.xlsx', sheet_name ='Burn Rates')
current_inventory_df = pd.read_excel('Model_Input_Seattle_Example.xlsx', sheet_name ='Current Inventory')

#clean data: remove spaces and capitalization
demand_sources_df.columns = map(str.lower, demand_sources_df.columns)
demand_sources_df.columns = demand_sources_df.columns.str.replace(" ", "_")

items_df.columns = map(str.lower, items_df.columns)
items_df.columns = items_df.columns.str.replace(" ", "_")
items_df.columns = items_df.columns.str.replace("(", "")
items_df.columns = items_df.columns.str.replace(")", "")

burn_rates_df.columns = map(str.lower, burn_rates_df.columns)
burn_rates_df.columns = burn_rates_df.columns.str.replace(" ", "_")
burn_rates_df = burn_rates_df.rename(columns={'daily_burn_rate': 'mean_daily_burn_rate'})

current_inventory_df.columns = map(str.lower, current_inventory_df.columns)
current_inventory_df.columns = current_inventory_df.columns.str.replace(" ", "_")
current_inventory_df = current_inventory_df.rename(columns={'amount_(units)': 'starting_inventory'})

#get options
options_df = pd.read_excel('Model_Input_Seattle_Example.xlsx', sheet_name ='General')
state_id = options_df[options_df['Unnamed: 0'] == 'State'].values[0][1]
county_id = options_df[options_df['Unnamed: 0'] == 'County'].values[0][1]
start_date = options_df[options_df['Unnamed: 0'] == 'Start Date'].values[0][1]
end_date = options_df[options_df['Unnamed: 0'] == 'End Date'].values[0][1]
warehouse_capacity = options_df[options_df['Unnamed: 0'] == 'Warehouse Capacity (in sq ft)'].values[0][1]
budget = options_df[options_df['Unnamed: 0'] == 'Budget'].values[0][1]
time_eval_days = (end_date-start_date).days


# In[5]:


burn_rates_df = pd.merge(burn_rates_df, current_inventory_df[['demand_source_id', 'item_id', 'starting_inventory']],
                         how='left',
                         left_on=['demand_source_id', 'item_id'],
                         right_on = ['demand_source_id', 'item_id'])


burn_rates_df['starting_days_inventory_left'] = burn_rates_df['starting_inventory']/burn_rates_df['mean_daily_burn_rate']
burn_rates_df['max_daily_burn_rate'] = burn_rates_df['mean_daily_burn_rate']*(1+max_adj)
burn_rates_df['min_daily_burn_rate'] = burn_rates_df['mean_daily_burn_rate']*(1-min_adj)


# In[6]:


burn_rates_df.head()


# In[7]:


#calculate total demand per day
burn_rates_df_grouped = burn_rates_df[['item_id', 'mean_daily_burn_rate',
                                       'min_daily_burn_rate', 'max_daily_burn_rate', 'starting_inventory']]\
.groupby(['item_id']).sum()

#only include consistent items that are not random by request(current assumption)
#burn_rates_df_grouped = burn_rates_df_grouped[burn_rates_df_grouped['mean_daily_burn_rate'] > 0]


# In[8]:


items_df = pd.merge(items_df, burn_rates_df_grouped,
                    how='left',
                    left_on=['item_id'],
                    right_on = ['item_id'])

#only dealing with consistently request items (for now)
items_df = items_df[items_df['mean_daily_burn_rate'] > 0]
items_df = items_df[items_df['mean_daily_burn_rate'] > 0]
items_df = items_df[items_df['item_id'] != 19]


# In[9]:


items_df


# In[10]:


def initialize_model(items_df_scenario):

    global time_eval_days
    model = ConcreteModel()

    #sets
    model.I = Set(initialize = items_df['item_id'])
    model.T = Set(initialize = range(1,time_eval_days))

    #penalty param
    def priority_initialize(model, i):
        value = items_df_scenario.loc[items_df_scenario['item_id'] ==i, ['priority_rank']].values[0][0]
        return(1/value)

    model.penalty = Param(model.I, initialize = priority_initialize)

    #size param
    def size_initialize(model, i):
        value = items_df_scenario.loc[items_df_scenario['item_id'] ==i, ['size_sq_ft_per_unit']].values[0][0]
        return(value)

    model.size = Param(model.I, initialize = size_initialize) #size of item

    #warehouse space cap
    model.warehouse_cap = Param(initialize = warehouse_capacity) #warehouse capacity

    #budget
    model.budget = Param(initialize = budget)

    #beggining inventory
    def beggining_inventory_initialize(model, i):
        value = items_df_scenario.loc[items_df_scenario['item_id'] ==i, ['starting_inventory']].values[0][0]
        return(value)

    model.starting_inventory = Param(model.I, initialize = beggining_inventory_initialize)

    #demand (note this will be dynamic when add t...)
    def demand_initialize(model, i, t):
        value = round(items_df_scenario.loc[items_df_scenario['item_id'] ==i, ['daily_burn_rate']].values[0][0],0)
        return(value)

    model.demand = Param(model.I, model.T, initialize = demand_initialize) #demand per day

    #delay time
    #def delay_initialize(model, i):
    #    value = items_df_scenario.loc[items_df_scenario['item_id'] ==i, ['delay']].values[0][0]
    #    return(value)

    #model.delay = Param(model.I, initialize = delay_initialize) #planned delay

    def price_initialize(model, i):
        value = items_df_scenario.loc[items_df_scenario['item_id'] ==i, ['price_per_unit']].values[0][0]
        return(value)

    model.cost = Param(model.I, initialize = price_initialize) #planned cost


    def supplier_capacity_initialize(model, i):
        value = items_df_scenario.loc[items_df_scenario['item_id'] ==i, ['supplier_capacity']].values[0][0]
        return(value)

    model.supplier_cap = Param(model.I, initialize = supplier_capacity_initialize) #capacity per week

    #variables
    model.units_of_stock_available = Var(model.I, model.T, within = NonNegativeReals)
    model.units_of_stock_allocated = Var(model.I, model.T, within = NonNegativeReals)
    model.units_of_stock_recieved = Var(model.I, model.T, within = NonNegativeReals)
    model.open_request = Var(model.I, model.T, within = NonNegativeReals)

    return(model)


# In[11]:


def initialize_objective(model):
    model.Objective = Objective(expr = (sum(model.penalty[i]*
                                            sum(model.open_request[i, t] - model.units_of_stock_allocated[i, t]
                                                for t in model.T) for i in model.I)),
                                sense = minimize)

    return(model)


# In[12]:


def initialize_constraints(model):

    global time_eval_days

    #set beggining inventory
    def initialize_beggining_inventory_constraint(model, i):
        return(model.units_of_stock_available[i,1] == model.starting_inventory[i])

    model.beggining_inventory_constraint = Constraint(model.I, rule = initialize_beggining_inventory_constraint)

    #calculate beggining of inventory daily
    def initialize_stock_availability_constraint(model, i, t):
        if(t > 1):
            return(model.units_of_stock_available[i,t-1] -
                   model.units_of_stock_allocated[i,t-1] +
                   model.units_of_stock_recieved[i, t-1] ==
                   model.units_of_stock_available[i,t])

        else:
            return(Constraint.Skip)


    model.stock_availability_constraint = Constraint(model.I, model.T,
                                                     rule = initialize_stock_availability_constraint)
    #calculate open requests
    def initialize_open_request_constraint(model, i, t):
        if t == 1:
            return(model.open_request[i,t] == model.demand[i,t])

        else:
            return(model.open_request[i,t] == sum(model.demand[i,t2] -
                                                  model.units_of_stock_allocated[i,t2]
                                                 for t2 in list(range(1,t))))

    model.open_request_constraint = Constraint(model.I, model.T,
                                               rule = initialize_open_request_constraint)

    #allocate supplies
    #cannot allocate more than available
    def initialize_allocation_constraint_1(model, i, t):
        return(model.units_of_stock_allocated[i, t] <= model.units_of_stock_available[i,t])

    model.allocation_constraint_1 = Constraint(model.I, model.T, rule = initialize_allocation_constraint_1)

    #cannot allocate more than open requests
    def initialize_allocation_constraint_2(model, i, t):
        return(model.units_of_stock_allocated[i, t] <= model.open_request[i,t])

    model.allocation_constraint_2 = Constraint(model.I, model.T, rule = initialize_allocation_constraint_2)

    #order supplies
    #cannot order more than supplier capacity per week
    def initialize_supplier_capacity(model, i, t):
        if t <= time_eval_days - 7:
            return(sum(model.units_of_stock_recieved[i, t]
                   for t in list(range(t,t+7))) <= model.supplier_cap[i])
        else:
            return(Constraint.Skip)

    model.supplier_capacity_constraint = Constraint(model.I, model.T, rule = initialize_supplier_capacity)

    #warehouse capacity
    def initialize_warehouse_capacity_constraint(model, t):
        return(sum(model.size[i]*model.units_of_stock_available[i,t] for i in model.I) <= model.warehouse_cap)

    model.warehouse_capacity_constraint = Constraint(model.T, rule = initialize_warehouse_capacity_constraint)

    #budget constraint
    def initialize_budget_constraint(model):
        return(sum(model.cost[i]*model.units_of_stock_recieved[i,t]
                   for i in model.I for t in model.T) <= model.budget)

    model.budget_constraint = Constraint(rule = initialize_budget_constraint)

    return(model)


# In[13]:


#for s in scenarios:
#    if s == 'min': (first run only min)
items_df_scenario = items_df[['item_id', 'size_sq_ft_per_unit',
                              'priority_rank',
                              'min_price/unit', 'min_delay_time',
                              'supplier_capacity', 'min_daily_burn_rate',
                              'starting_inventory']]

items_df_scenario = items_df_scenario.rename(columns={'min_daily_burn_rate': 'daily_burn_rate'})
items_df_scenario = items_df_scenario.rename(columns={'min_price/unit': 'price_per_unit'})
items_df_scenario = items_df_scenario.rename(columns={'min_delay_time': 'delay'})

model = initialize_model(items_df_scenario)
model = initialize_objective(model)
model = initialize_constraints(model)


# In[14]:


opt = SolverFactory('gurobi_persistent')
opt.set_instance(model)
opt.solve(model)
