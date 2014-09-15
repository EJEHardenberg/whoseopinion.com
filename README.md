whoseopinion.com
================

Open Code for an Open Opinion Site. 


Technologies:
-----------------------------------------------------------------------

- [Harp]
- [Django]
- [Apache]

Installation and Setup:
-----------------------------------------------------------------------

For setting up [Harp], [Django], or [Apache] please visit their
respective sites and follow their instructions.

Once [Harp] is installed, run `harp compile` from the root of the
repository to be sure that the static files are up to date. If you are
changing the name of the site to something else, update the _harp.json_
file as appropriate.

Next, install [virtualenvwrapper] and create a virtual environment for
your python files. While using `workon` you can run `pip install -r
requirements.txt` to install the neccesary modules to run the [Django]
API server.

Finally, setup an [Apache] environment which serves the Harp's *www*
directory and proxy pass's to the Django server like so:

    <VirtualHost *:80>
	            ServerAdmin webmaster@localhost
	            ServerName dev.whoseopinion.com
	 
	            DocumentRoot /path/to/the/repo/www
	            <Directory />
	                    Options Indexes
	                    AllowOverride None
	            </Directory>
	 
	            ProxyPass /api http://localhost:8000/questions/
	            ProxyPassReverse /api http://localhost:8000/questions/
	</VirtualHost>

You'll need to do a `workon <environment>` and a `fab runserver` from 
the api directory before you start apache for the ProxyPass to work 
correctly.


Note that at this time, the use of [Apache] is for development only.
A soon to come production environment may use different technologies
such as [nginx] and [gunicorn]. 

[Harp]:http://harpjs.com
[Django]:https://www.djangoproject.com/
[Apache]:http://www.apache.org/
[virtualenvwrapper]:http://virtualenvwrapper.readthedocs.org/en/latest/install.html
[nginx]:http://nginx.com/
[gunicorn]:http://gunicorn.org/
