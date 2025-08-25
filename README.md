# kbmd
Knowledgebase markdown CLI tool

I am considering creating a new command line interface tool called kb that helps people create and manage "knowledgebases" from the command line but I want to be careful not to reinvent the wheel.
The idea of this tool is to help manage metadata about shared files and folders. 

For example in my use case I help researchers in a biology lab keep track of data on a shared HPC cluster. 
We have access to folders on multiple file-systems, say /scratch, /projects, and /cold. We also have data in cloud storage.
It can be difficult to remember what datasets are a where which sometimes leads to multiple researchers downloading their own copies of the same large files which can lead to file system issues and makes collaboration difficult. Furthermore, it's not uncommon to find a large subfolder say /projects/myproject1 created by a researcher that stores 20TB of data and scripts, but doesn't have a README or any associated metadata.

I am thinking that the "knowledgebase" in this case would be a collection of markdown files with a standardized schema.
Maybe there would be one markdown file per "project" or "dataset" and there would be fields such as "data size" and "data source" and "general description".
There could also be "table of contents" markdown files say for different topics or different file systems such as /projects which would link to the per-project/per-dataset markdown files.
I am thinking of using markdown since I'd be able to have these files inside a git repository and have a nice browsing experience on github with relative-linked markdown files.
This would also allow people to edit the files directly on github after they are setup from the command line.

There is nothing stopping me from creating these markdown files by hand, but whenever there is a new project I will need to manually create a new markdown file and make sure to link it into the knowledgebase of other markdown files.
I will also need to be careful and enforce the markdown schema by hand to make sure I don't leave out any "required" information.
I'd like the other researchers to be able to easily add to the knowledgebase.
For these reasons I'm considering to use a tool to help manage the knowledgebase, and since most users interact via command line I think a CLI tool would be a good fit.
This situation feels similar to a static website generator.

While ssh'd into the cluster I'd like the user to be able to run a command like `kb add .` from the root of a directory such as /project/important-project-37 and be prompted
to fill out metadata information that will be used to create a valid markdown file that is added to the knowledgebase collection of markdown files locally.
Then they could maybe run `kb push` which would make any changes necessary to the local knowledgebase to result in a git push to make their changes available on github, and/or return an error.
There could also be a command `kb fresh` which would cause the knowledgebase to check that all file-paths in the metadata still exist and/or update file sizes and last-modified times.

The reason I'm considering using github as the frontend of the knowledgebase is that all our coworkers have access to a shared github organization so that we can have a knowledgebase that is private but browseable.
Also I do not have web development experience so I'd like to keep the interface as simple as possible.
Because we are only storing metadata I don't think we'll need an external database.

Some questions I need to answer are if there is already a way of using an existing tool, such as a static site generator to achieve these goals
and if there are conceptual issues with this approach of implementing a knowledgebase.
