Welcome to the Judge Pics Repository
====================================

This is a collection of judicial profile pics that can be cloned and used in any project. Original files can be found in the `orig` directory and converted versions can be found in the numerical directories.

The goal of this project is to collect and maintain an updated repository of all important judges over the years.


Contributing
------------

This project is blissfully easy to contribute to and we need lots of help
gathering files. The process for this is pretty simple.

1. Find an image and ensure it follows our quality guidelines
(below).

1. Add the image file to the `orig` directory.

    Pictures are given the name of the judge and are of in the form:

        $last-$first-$suffix-$dob.jpeg
    
    Where $dob is only necessary in the case of duplicates. So, for example 
    Sonia Sotomayor would be:

        sotomayor-sonia.jpeg
    
    Note that the date is in ISO-8601 format, the name is lowercase, and the 
    extension is `jpeg`, not `jpg`.
    
    Some judges may have multiple great portraits. For those, place a number 
    after their name such as:
     
        sotomayor-sonia-2.jpeg
        
    
1. Regenerate the converted versions by running `convert_images.py` (note that
this requires `imagemagick`).

1. Edit `judges.json` to include the relevant fields for your new file such as 
   the source and the license.

That's it!


Quality Guidelines
------------------

1. Trim any extraneous margins so that the judge's head and shoulders are visible. 
1. Images must be `jpeg` file format.
1. Images must be in the public domain or you must dedicate them there, if you took the image yourself.


Installation
------------

Basic usage doesn't require any installation, but if you wish to import the `judges.json` file into a Python program, you may want to install this as a Python module in your system. To do so:

    sudo git clone https://github.com/freelawproject/judge-pics /usr/local/judge_pics
    sudo ln -s /usr/local/judge_pics /usr/lib/python2.7/dist-packages/judge_pics

You can then import the `judges.json` information into your project using:

    from judge_pics import judge_pics


Copyright
---------

Two things. First, if you are creating original work, please consider signing
and emailing a contributor license to us so that we may protect the work later,
if needed. We do this because we have a lot of experience with IP litigation,
and this is a good way to protect a project.

Second, if you're just curious about the copyright of this repository, see the
License file for details. The license of individual images is described in 
`judges.json`.
