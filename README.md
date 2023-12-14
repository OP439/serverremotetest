This file lives on an ec2 instance on aws. 

It was very useful to set github up on the remote instance also so that the terminal-based nano code editor did not have to be used to make updates to the code.

One thing that had to be checked was that certificates being used to authenticate the user for the cloud processes were not committed to a public repo. 

These repos will probably be made private again once marked so that there is an extra security buffer in between. 

Bootstrap was used to make the website look nicer as it could be included with a link and no files needed to be transferred across. This could be a risk if Bootstrap ever shuts those links down as then all the formatting of the website will be gone. 
