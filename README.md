
Welcome to the Judge Pics Repository
====================================

This is a collection of judicial profile pics or portraits that can be used in any project. Original files can be found in the `orig` directory and converted versions can be found in the numerical directories.

The goal of this project is to collect and maintain an updated repository of all important judges over the years. There are two types of pictures in this repository. The first are head shots or portraits of judges, and the second are group shots of the entire bench on a specific date.


Contributing as a Developer
---------------------------

This project is fairly easy to contribute to and we need lots of help gathering files. You can see untapped sources for images in the [additional-sources.md][add] file.

The process for this is pretty simple, but if you need help or just want to email us photos, that works too. Just get in touch via [our contact page][contact].

The normal process is:

1. Find an image and ensure it follows our quality guidelines
(below).

1. Add the image file to the `orig` directory.

    Pictures are given the name of the judge and are of in the form:

        $last-$first-$dob.jpeg

    Where $dob should be completed to the highest possible granularity. So, for
    example Antonin Scalia, a well-known judge would be:

        scalia-antonin-1936-03-11.jpeg

    Noting that:

    - birth dates should be [set using ISO-8601 format][8601] and should be
      provided at the highest possible granularity. I.e., if only the year
      is known, then only the year should be provided.
    - the name is lowercase.
    - the extension is `jpeg`, not `jpg`.
    - any punctuation marks in a judge's name should be elided or converted to
      a dash, according to [Django's slugify function][slugify].

    For example:

        oconnor-sandra-1930-03-26.jpeg

    Some judges may have multiple great portraits. For those, omit the date of
    birth and place a number after their name such as:

        sotomayor-sonia-2.jpeg

    We have also begun collecting group pictures. For these, the pattern is:

        group-$court-code-$date.jpeg

    Noting that:

    - `$court` corresponds to the Juriscraper/CourtListener code for the court.
      If you are unsure what code to use, you can [easily look it up on
      CourtListener][codes].
    - The date should be the earliest date that a group of judges is known to
      work together. In many cases, you'll be unsure and will need to simply use
      today's date. That's OK. Again, [dates should be in ISO-8601
      format][8601].
    - Again, the extension is `jpeg`, not `jpg`, and certainly not `png`.


1. Regenerate the converted versions by running `convert_images.py` (note that
this requires `imagemagick` and `exiftool`).

1. Edit `judges.json` to include the relevant fields for your new file such as
   the date of the portrait, source, artist, and license. (By default, the
   license field is set to "Work of Federal Government", as these photos are
   the easiest to procure.)

That's it!


Quality Guidelines
------------------

1. Images should be a head and shoulders shot of the judge.
1. Images must be `jpeg` file format.
1. Pictures of painted portraits are often skewed and often show the wall where
   the portrait is hung. Before submitting, de-skew the image and crop out
   any bits of wall that you can see around the edges.


Installation
------------

Basic usage doesn't require any installation, but if you wish to import the
`judges.json` file into a Python program, you may want to install this as a
Python module in your system. To do so:

    git clone https://github.com/freelawproject/judge-pics
    sudo python setup.py install

You can then import the `judges.json` information into your project using:

    from judge_pics import judge_pics


A Note to Judges
----------------
If you're a judge looking at this, and you want your picture to be included too,
you can contribute it yourself using the guidelines in this readme.

Alternatively, if you prefer, you can [send us an email using the contact form
on the Free Law Project website][contact], and we'll be happy to do it for you.

Either way, we'd be elated to hear from you.


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
[slugify]: https://docs.djangoproject.com/en/1.8/_modules/django/utils/text/#slugify
[8601]: http://en.wikipedia.org/wiki/ISO_8601
[contact]: http://free.law/contact/
[codes]: https://www.courtlistener.com/api/jurisdictions/
