Apache_Tester is a free to use python script that was created as part of a capstone project. 
This program is meant to be used only with linux machines running apache web servers (apache2 or httpd).

In the current version (v0.5), basic operations of the script have been completed and can be ran 
with terminal input.

All required files can be found in the 'build' directory as a zip file to be downloaded. 
Once downloaded, unzip the 'current_build.zip' file in a directory of your chice, and give execute 
priveleges (chmod -x <file_name>) to the included 'apache_tester.py' file. From here all you need 
to do is execute it.

---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

The script operates with arguments:

  -c, --change: 
      Allows the script to automatically change settings to match best practices
      
  -p, --printReport: 
      Prints a report showing the items meeting industry best practices, followed by those that don't
      
  -s, --silent: 
      Turns off confirmation prompts before making each change
      
  -v, --verbose: 
      Enables verbose mode

If you are using -c/--change mode, when the following settings are found to not meet best security 
practives, you will be prompted to either change the setting to meet best practices, or to keep the 
setting as is (with a yes or no terminal input). 
*Note - this only works when running the program with sudo or root access.

No matter what you choose, as best practice, a backup of your current configuration files (before 
edits are made) can be found in the programs current directory.

---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

The included script currently locates configuration files and version numbers of apache on the host 
machine (mainly apache2.conf/ httpd.conf and security.conf apache files). These files are then 
scanned for the information below.


  Apache Version  
====================

Latest versions of software can include important updates such as security patches and bug fixes. 
It is important to stay up to date with new releases. 

Apache_Tester checks your currently installed version of apache2 or httpd and compares it to 
the most recent release



  Server-Info  
=================

Displays information about the Apache configuration when the /server-info page is accessed from 
http://www.example.com/server-info. This could potentially include sensitive information about 
server settings such as the server version, system paths, database names, library information, etc. 
This should be commented out to avoid providing additional information on server systems to threat 
actors.

Apache_Tester checks for the “<Location /server-info>” setting and will commented it out.



  Signature  
===============

While turned on, ServerSignature provides the server version number and server name to the footer line. 

Apache_Tester checks for the “ServerSignature” option in the security configuration file and will 
set it to “off”.



  Banner  
============

When enabled, this option includes a description of the generic OS-type of the server as well as 
information about compiled-in modules in the banner returned to the client.

Apache_Tester checks for the “ServerTokens” option in the security configuration file and will 
set it to “Prod".



  Trace HTTP Requests  
=========================

Trace is a HTTP request method used for debugging that sends back an input to the user. This method 
creates the possibility for security vulnerabilities that could be exploited to access cookies or 
website credentials via the header.

Apache_Tester checks for the “TraceEnable” option in the security configuration file and will set it 
to “off”.



  Timeout Value Configuration  
=================================

A server connection timeout occurs when a server is taking too long to reply to a data request. 
The Timeout option sets the number of seconds the server will wait before it receives and sends a time out. 
By default, apache sets this number to 300, which is vulnerable to Slow Loris and Denial of Service attacks.

Apache_Tester checks the configuration file for the current timeout setting, and will change the duration 
to 60 seconds.
