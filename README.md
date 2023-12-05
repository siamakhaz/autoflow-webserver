**Table of Contents**  

- [Docker](#docker)
- [Docker Compose](#docker-compose)
- [Apache Configs](#apache-configs)
- [Updater](#updater)
- [Did you fork this project?](#did-you-fork-this-project)
- [Troubleshooting](#troubleshooting)


# Docker
This is a Dockerfile that starts with an `httpd:latest` image and configures it with the following commands:

- `COPY` copies the `httpd.conf` file from the current directory to `/usr/local/apache2/conf/httpd.conf` inside the image.
- `RUN` creates a directory `/usr/local/apache2/conf/sites/` inside the image.
- `EXPOSE` exposes ports 80 and 443.
- `CMD` sets the default command for the container to `httpd -D FOREGROUND`, which starts the Apache web server and keeps it running in the foreground.

This Dockerfile is used to create a custom image with an Apache web server configured with the `httpd.conf` file provided. The resulting image can be used to launch containers that serve web content.

# Docker Compose
This is a Docker Compose file written in version 3.8 format. It defines a service named `octdocs` with the following configuration:

- The service uses an `httpd-server` image.
- The image is built using the Dockerfile in the current directory (`build: .`).
- The service exposes two ports: `${dochttp}` mapped to port 80 and `${dochttps}` mapped to port 443. These ports are specified as environment variables.
- The container is named `httpd-docs`.
- The service mounts two volumes:
  - `./sites/` on the host machine is mounted to `/usr/local/apache2/conf/sites` inside the container.
  - `./public/` on the host machine is mounted to `/usr/local/apache2/htdocs` inside the container.
- The service is set to `restart: always`, which means that it will automatically restart if it stops for any reason.

# Apache Configs
## SSL

This code sets up a virtual host to listen on port 443 with HTTPS protocol. The SSLCryptoDevice is set to "builtin".

The configuration specifies that the SSL engine should be enabled for the virtual host, and for specific file types, SSL options with standard environment variables should be used. The document root is set to `/usr/local/apache2/htdocs` with the directory options set to allow indexing, following symbolic links, and no override. Access is allowed to all users.

The browser match rule disables keep-alive for Microsoft Internet Explorer versions 2 through 5, and forces a response of version 1.0.

The SSL certificate files are specified, including the certificate file, certificate key file, and certificate chain file. The SSL proxy engine is also enabled.

Finally, the server name is set to `sub.example.com`, and the server administrator email is set to `maintainer@example.com`.

In summary, the code is an Apache configuration that enables SSL for a virtual host listening on port 443 with HTTPS protocol. It sets the SSLCryptoDevice to "builtin" and specifies SSL options for specific file types. The document root is set to "/usr/local/apache2/htdocs" with directory options allowing indexing, following symbolic links, and no override. A browser match rule disables keep-alive for older Internet Explorer versions and forces a response of version 1.0. SSL certificate files are specified, and the SSL proxy engine is enabled. Finally, the server name and administrator email are set.

## HTTP

This code sets up a virtual host to listen on port 80. The server name is set to "sub.example.com". It then performs a permanent redirect to "https://sub.example.com/" using the Redirect directive.

The AllowEncodedSlashes directive is then enabled, which allows encoded slashes to be passed in the URL path, which is useful in some cases.

Finally, the RewriteEngine directive is enabled, which allows for URL rewriting using regular expressions.

In summary, the code sets up a virtual host to redirect traffic to the HTTPS version of the site and enables the AllowEncodedSlashes and RewriteEngine directives.

# [Updater](./Updater/Readme.md)

This is a simple webhook designed to execute updates on the production environment in response to Bitbucket webhook events. 

Specifically tailored to react to push and merge actions on the master branch, the Python script employs a Flask web server to monitor these events. 

Upon detection, it performs a git pull in a specified directory, ensuring the production environment is synchronized with the latest changes. 

Additionally, after each update, the script communicates back with Bitbucket, updating the build status of the respective commit, thus maintaining a clear record of deployment statuses in the repository.

# Did you fork this project?

note that you need to remove the .git and update your project based on your repo provider

The above example expects to put all your HTML files in the `public/` directory.

You also need to call a webhook https://sub.example.com/update to update the project.

# Troubleshooting

1. CSS is missing! That means that you have wrongly set up the CSS URL in your
   HTML files. Have a look at the [index.html](./public/index.html) for an example.


