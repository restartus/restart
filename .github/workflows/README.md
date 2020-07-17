# Github Actions

These are basic CI/CD actions. The test first failed with the idea that you just
create a file in .github/workflow and it just works. This doesn't seem to be the
case. You have to create the file at https://github.com in the actions tab by
selecting new workflow. This uses the [XL Trail GitHub
Actions](https://www.xltrail.com/blog/how-to-manage-and-release-excel-files-on-github-part2)

The sample uses `name` to give a name to the workflow section.

## Setting up for this

We use environment variables in the files to set things up, so set
RELEASE_SPREADSHEET at the top and it should work.

## The workflows

- Test.yml. This just runs with master and verifies that the build is working.
  You should see it runnin under the action tab
- Upload.yml. This is the test version. Any time it sees a release it will run
  and upload the right files
- Upload-tag-to-release.yml. This takes any tag that it sees and makes it a
  release. Useful if you don't want to hit the UI.
- Upload-xltrail.yml. another verification, it is code copied from XLTrail.com

# Notes on debugging


In the original XLTrail example it didn't work

So first we got the basic test to work

This started to work, but you need to have a flag on checkout.
https://stackoverflow.com/questions/61463578/github-actions-actions-checkoutv2-lfs-true-flag-not-converting-pointers-to-act

so in the add the following lines

## Dealing with git lfs

The main lesson here is not to do the with lfs because this checks out the whole
repo which is very slow

```
step:
  - names: checkout with lfs
    uses: actions/checkout@v2
    with:
      lfs: true
```

Instead, you do not want to set that and just run a pull for the file that you
need
```
  - name: Checkout LFS object
    run: git lfs pull --include="file that you need"
```

## What's up with releases and tags

These are two different things. A
[tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
is something that you can do from the
command line. A [release](https://help.github.com/en/github/administering-a-repository/managing-releases-in-a-repository)
is a Github thing and is for managing above the level of
releases. there is user interface for modifying and deleting them. Alghout this
is a big tricky. It is at the upper right of the release page

For releases, when you create you, you specify a commit and then a branch and
when this happens, you will get a set of assets. The default is a zipped copy of
the source code.

But with Github Actions, you can load whatever you want.

So to create tags, it takes two steps first locally,

```
git tag -a v1.2 -m "Latest updates and fixe"
git push origin v1.2
```

## Looking at runs

There are few things, you will see a list of named runs. You can rerun any run
that you like, but you can't change the Workflow file if you've made edits.
