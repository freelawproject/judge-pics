
# Welcome to the Judge Pics Repository

This is a collection of judicial portraits that works in tandem with the Free Law Project judicial portraits hosted photo service. You can use this system to integrate picture of judges directly into your applications.

Original files can be found in the `orig` directory.


## Using this Project

This system is exceedingly simple. To use this it, install the judge pics package from pypi:

    pip install judge-pics

And then use that package to get the URL of a judge's portrait. You can do that in one of two ways. You can look up the judge by name:

    >>> from judge_pics.search import portrait, ImageSizes
    >>> portrait("Ketanji Jackson", ImageSizes.SMALL)
    'https://portraits.free.law/v2/128/jackson-ketanji-1970.jpeg'

Or if you know the CourtListener ID for that judge, that works too (and is more reliable). Ketanji Jackson is ID 1609, so:

    >>> portrait(1609, ImageSizes.SMALL)
    'https://portraits.free.law/v2/128/jackson-ketanji-1970.jpeg'

Now that you have the URL of the judge's photo in a useful size, just embed it in your application. Perhaps:

```html
<img src="'https://portraits.free.law/v2/128/jackson-ketanji-1970.jpeg"/>
```

Simple enough. The URLs we provide you will be reliable, performant, secure, and permanent (see below for details).

You can request images in one of the following sizes:

```python
class ImageSizes(Enum):
    SMALL = 128
    MEDIUM = 256
    LARGE = 512
    ORIGINAL = "orig"
```

Selecting `ImageSizes.ORIGINAL` will give you a link to the original image that we have in our collection. You'd want to use this to make custom sized images, say.

Finally, if you're debugging or playing around, you can get a feel for a picture by using the `show` function:

![Judge Jackson as ANSI escape codes](https://github.com/freelawproject/judge-pics/blob/main/show-jackson.png)

That's about it.


## FAQs

### How reliable is the service?

Very. It uses AWS S3 with CloudFront as a CDN. That gives us a LOT of of nines.

### What about versioning? 

Over time, we will be adding more photos to these collections. These will arrive as updates to the Python package and as new photos in the service. We expect these to be generally backwards compatible, but if we need to break compatibility, we will do so by bumping the Python package to version 3.x, and changing the URL of the images to contain v3 instead of v2.

We see no reason why past URLs will ever change.

### So this is a free service? Huh?

Hosting this service is cheap, so we're just going to do it. That said, collecting the images for this service and developing it is extremely expensive. Some of this work was supported by Pre/Dicta, but donations help offset our costs.

Please [donate][d] if this is useful to you.

### How secure is this?

Here's how we're thinking about it.

**1. What prevents the images from being replaced with malicious ones?**

The short answer is that our incentives are aligned with yours. Because our website uses this same service, it would be difficult for an attacker to put malicious photos on your website without them also appearing on ours. This service is included in our [vulnerability disclosure policy][vdp], and we use process and technical measures to prevent incidents.

In browsers, there is some discussion of a way to use cryptographic signatures to ensure the integrity of hotlinked images, but the feature has not seen much support. ([We're trying to nudge it along.][spec])


**2. What private information would we share with Free Law Project by using these services?**

Two pieces of data are shared with us:

1. The IP address of your users.

2. The URL and/or domain of your website via `referer` headers.

Ideally, we wouldn't get either of these pieces of information, but we at least need the IP so we can serve the request. We do not log it.

For the referrer, you can avoid sharing it with us by setting the [`Referrer-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) header on your website. You should probably do this anyway.


**3. What if Free Law Project is hacked? Could that hack me too?**

The short answer is "not really." If you're using the `<img>` tag to put judge portraits or court seals on your website, the worst a hacker can do is change those photos. That's not great but the hacker couldn't deliver malicious javascript to your users, couldn't access private information from your website, etc. Hotlinking photos is as old as the Web itself and remains generally secure.


## Contributing as a Developer

This project is fairly easy to contribute to and we need lots of help gathering files. You can see untapped sources for images in the [additional-sources.md][add] file.

The normal process is:

1. Find an image and ensure it follows our quality guidelines (below).

1. Add the image file to the `orig` directory.

    Pictures are given the name of the judge and are of in the form:

        $last-$first.jpeg

    Noting that:

    - the name is lowercase.
    - the extension is `jpeg`, not `jpg`.
    - any punctuation marks in a judge's name should be converted to
      a dash, according to [Django's slugify function][slugify].

    For example:

        oconnor-sandra.jpeg

    Some judges may have multiple great portraits. For those, omit the date of
    birth and place a number after their name such as:

        sotomayor-sonia-2.jpeg

    We have also begun collecting group pictures. For these, the pattern is:

        group-$court.jpeg

    Noting that:

    - `$court` corresponds to the CourtListener code for the court.
      If you are unsure what code to use, you can [easily look it up on
      CourtListener][codes].
    - Again, the extension is `jpeg`, not `jpg`.


1. Once you have the picture ready, run `python update.py --help` and it'll guide you through the process of updating `people.json`.


## Quality Guidelines

1. Images should be a head and shoulders shot of the judge.
1. Images must be `jpeg` file format.
1. Pictures of painted portraits are often skewed and often show the wall where
   the portrait is hung. Before submitting, de-skew the image and crop out
   any bits of wall that you can see around the edges.


## New Releases

New releases are fairly seldom. When they happen, the version number is bumped in setup.py, and a new tag matching that version number is added to git. When it's pushed, images are automatically uploaded to S3 and a new release is pushed to PyPi.


## A Note to Judges

If you're a judge looking at this, and you want your picture to be included too, you can contribute it yourself using the guidelines in this readme. We enthusiastically encourage you to do so.

Alternatively, if you prefer, you can [send us an email using the contact form on the Free Law Project website][contact], and we'll be happy to do it for you.

Either way, we'd be elated to hear from you.


## Copyright

Two things. First, if you are creating original work, please consider signing
and emailing a contributor license to us so that we may protect the work later,
if needed.

Second, if you're just curious about the copyright of this repository, see the
License file for details. The license of individual images is described in
`people.json`.


[add]: https://github.com/freelawproject/judge-pics/blob/master/additional-sources.md
[slugify]: https://docs.djangoproject.com/en/1.8/_modules/django/utils/text/#slugify
[contact]: http://free.law/contact/
[codes]: https://www.courtlistener.com/api/jurisdictions/
[d]: https://free.law/donate/
[spec]: https://github.com/w3c/webappsec-subresource-integrity/issues/113
