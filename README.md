Welcome to the Judge Pics Repository
====================================

This is a collection of judicial profile pics that can be cloned and used in any project. Original files can be found in the `orig` directory and converted versions can be found in the numerical directories.

The goal of this project is to collect and maintain an updated repository of all important judges over the years.


Contributing
------------

This project is blissfully easy to contribute to and we need lots of help
gathering files. You can see untapped sources for images in the 
[additional-sources.md][add] file. 

The process for this is pretty simple.

1. Find an image and ensure it follows our quality guidelines
(below).

1. Add the image file to the `orig` directory.

    Pictures are given the name of the judge and are of in the form:

        $last-$first-$suffix-$dob.jpeg
    
    Where $dob is only necessary in the case of duplicates. So, for example 
    Sonia Sotomayor would be:

        sotomayor-sonia.jpeg
    
    Note that dates should be set using ISO-8601 format, the name is lowercase, 
    and the extension is `jpeg`, not `jpg`. Any punctuation marks in a judge's
    name should be converted to a dash. For example:
    
        o-connor-sandra.jpeg
    
    Some judges may have multiple great portraits. For those, place a number 
    after their name such as:
     
        sotomayor-sonia-2.jpeg
        
    
1. Regenerate the converted versions by running `convert_images.py` (note that
this requires `imagemagick`).

1. Edit `judges.json` to include the relevant fields for your new file such as 
   the date of the portrait, source, artist, and license. (By default, the 
   license field is set to "Work of Federal Government", as these photos are 
   the easiest to procure.)

That's it!


Quality Guidelines
------------------

1. Images must be `jpeg` file format.
1. Pictures of painted portraits are often skewed and often show the wall where 
   the portrait is hung. Before submitting, de-skew the image and crop out 
   any bits of wall that you can see around the edges.
1. Images must be in the public domain or you must dedicate them there, if you 
   took the image yourself. Works of the Federal Government are in the public
   domain, so generally portraits of Federal judges can be included in this 
   collection.


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


[add]: https://github.com/freelawproject/judge-pics/blob/master/additional-sources.md
