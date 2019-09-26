# Installing Dependecies
ELang like all other programming languages need a special project setup to work correctly. And as so, you will also need some other 3rd party tools to be installed. ELang'c compiler sure do come as one single executable file as always. If know your ways and don't need help, this paragraph is for you. If you need help, then just skip it.

`ELang needs a G++ compiler to be setup either on path or somewhere known. on debian based systems, you can use apt-get to install g++ easily and on path. but for windows, you would need MingW64. If you don't want all the setup thing, you can also use ThreadCC on github! For threadCC make sure you write a batch code to open the command line of ThreadCC and the link it to the ELang on config.yml! You'll learn more on the way.`

Okay... that was long! so. here is a step by step on setting it up!

## Linux

I am not biased towards any system. but I am talking about linux first because it is the easiest way to setup!

All you have to do for installing dependencies is to fire up your terminal and executing:

`sudo apt-get install g++` on ubuntu

or

`su apt-get install g++` on debian

for any other distro, check on how they do their package managment!

## Windows
Now for windows... it is a bit tricky! I personally do not like visual studio's compiler as its not much flexible outside of visual studio so we will go with ThreadCC as it is best and easy as of now!

Go to [ThreadCC's Github](https://github.com/turbo/ThreadCC) and download it. You will see two [batch files](https://en.wikipedia.org/wiki/Batch_file). That is basically all! For now...

## MacOS

I do not have access to a Mac or their OS as of now so I personally do not know how things work there. But I think you might need to setup XCode! MacOS is not natively supported by ELang so you will need to do all parts yourself!

# Basic Setup

After you installed required dependencies, you are ready to use ELang! take the executable of ELang and put it in the folder you want to start your project on, say, `MyProj`.

You can now use ELang in these few steps:

1. Run the ELang compiler on empty folder once. You will see two files appearing going by names of `config.yml` and `compile.elpp`.<br><br>
`config.yml` is used for configuration of your project! <br>
`compile.elpp` is used for your main code! <br>
<br> NOTE: if you did not see anything happen while running the ELang for first time, try running it with admin access! some systems require it for security purposes!

2. Change the `config.yml` configuration on G++ path. If you are on linux, just leave it! if you are in windows and use ThreadCC, the path to g++ would look like for example `ThreadCC\x64\bin\g++.exe`. Copy that path and put it in the `config.yml` on the `G++Path` option. That is all!

3. Run ELang again. now you should see a file by name of `compile` on the folder! this shows that it was a success!<br><br>
Run the file and you should see a `Hello World!` on the screen!
<br><br> NOTE: If you did not see it, your g++ path might be wrong!