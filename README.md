# CSE4081 Term Project - Wiki Study Organizer

### Purpose:
The goal of this project is to create a tool that roughly organizes a set of wiki articles from least complex to most complex to assist with self-teaching. We plan for this project to be compatible with all articles in the wiki format, although we will specifically be focusing on the articles on chessprogramming.org.

### Install Instructions:
Make sure docker is installed then run start.sh on a Linux/MacOS machine.
This will install the relevent container & all related packages.
  Note: Docker alternatives (eg. Podman) may not run properly.

### Usage:
To use the program also run start.sh this will make sure the container is up to date and launch into it. Once started you can use the cmd to naviagte the menu to access things in your library or add more. To change the port on your host system you can add a cmd enviroment variable or change the one in start.sh. The default serve port is 38273 and should be accessable on localhost. To add your own wikis either use the built in zimit wrapper or drop .zim files in the library.

Also for development testing the start.sh script has a -b flag to start the container in bash and a -c flag to build it with no cache.
