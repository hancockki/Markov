# Creative Yoga Sequencing with Markov Chains

## Generate a unique yoga sequence using markov chains!
The purpose of this application is to generate a unique yoga class for yoga instructors to keep their sequencing creative. The motivation behind the app is that yoga instructors are always trying to come up with unique sequencing for their classes. In a yoga class, a sequence is basically a bunch of poses that flow together, with one pose transitioning seamlessly into the next. This app is based off a typical vinyasa yoga class, which you can read about [here](https://oneflowyoga.com/blog/what-is-vinyasa-yoga). The history of yoga resides in ancient South Asian religion, and has its origins in the Vedas, one of the first religious texts. However, the yoga practiced in the west today is very far from the ancient practice, and most western classes follow a similar vinyasa flow model. 

## Why this app?
As someone with years of yoga practice, I am always looking for new sequences for myself and the classes I teach. It is easy to just do the same sequences over and over, rather than mixing it up and finding new flows. Since yoga is all about transitioning from one pose to another, I thought that Markov chains could be applied to predict the probability of transitioning from one pose to the next. For example, almost every class starts with the Sun salutations sequence followed by a Warrior II sequence, so the probability of going from Down Dog to forward fold (which is part of the sun salutations sequence) is high. I thought it would be cool to see if a markov chain could generate a sequence of poses based on a starting pose and the probability of transitioning to any other pose from the starting pose, and continuing on in this way. For example, if we start in child's pose, there is a high probability that our next pose will be a seated position or cat cow pose, which are both warm-ups. The data set to predict the probabilities I took from past classes I have taught and done myself; the probability of transitioning from one pose to any other is calculated by adding up the number of times a given pose is followed by any other pose. Then, the markov chain will pick the next pose based on these probabilities. Once the app is run, a webpage is displayed with the sequence the markov chain generated. The user can then use this sequence or generate another!

Desigining the app was challenging because I was not sure how to incorporate the visual component of the app--most of the examples of markov visual art I looked at while brainstorming were based on manipulating existing images to rearrange the pixels. Since I had the idea to generate a yoga sequence, I decided to use images of every pose and display the sequence in a visually appealing way. The challenge was that I do not have very much experience with graphic design. I could have chosen to use an external collage maker, but I wanted the collage of poses to be dynamic and pop onto the screen immediately. For this reason I chose to develop an app and display the collage in a webpage using html and css. However, almost ALL of my coding experience is in backend development, so making the collage artistic turned out to be a big road blocker. I have really never used html or css, so I challenged myself in learning some new languages. I believe this app is creative since it may come up with sequences that a yoga instructor wouldn't necessarily think of. I also think it's creative because it has the potential to be developed further to make it more personalizable. As a proof of concept I really think this is a totally unique use of markov chains that can help foster creativity in yoga teaching. It could also be useful for people wanting to practice yoga on their own who don't have much experience with sequencing classes.

## Looking forward
Future developments for the app:
- Add more classes to my dataset to get better results
- Improve the frontend development and app structure
- allow the app to be more 'personalizable' (aka allow the user to specify what type of class they want in more detail). This is totally attainable since I already have all of the information associated with each pose saved in the app, but didn't end up having the time to use it that much. 

Future developments for my own coding:
- Keep trying to use css and html for web development
- understand the different components of building an app better, like how it connects to the server and how to use GET and POST requests

## How to set up and run the system
This system uses Django for web development to ultimately interact with the user and display the yoga class in the web browser. I chose this format to challenge myself as a coder and gain experience with web development, which I have not done much of. I used [this tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/) to help me build the app. 
To run the app yourself, first clone this repo by creating a new directory called Markov and then entering that directory. Then, use the following terminal commands:

1. git init 
2. git clone [this repo url]

This will create a local copy of this repo in the right directory. The file structure for the app is as follows:
* markov
  * yoga_markov
  * yoga
        * static
   * css
   * index1.html
   * init.py
   * admin.py
   * apps.py
   * asana_master_list.xlsx
   * models.py
   * tests.py
   * urls.py
   * views.py
   * migrations
  * yoga markov
   * settings.py
   * urls .py
   * wsgi.py
   * manage.py

The most important files here (the only ones i modified from the starter app) are the yoga_markov/yoga/static folder, which contains all the images and static css, views.py, settings.py, and models.py. I also created index1.html which displays the page. 

To run this, navigate to Markov/yoga_markov directory. Also, make sure all of your dependencies have been met (aka you have pip installed all needed packages). Most notably used are django and xlrd. Everything else should be fine, but you will get errors for unmet dependencies and can simply install them using "pip3 install [package name]" in the terminal.
Then, in the yoga_markov directory, type the following in the terminal to start the app:

python3 manage.py runserver

IMPORTANT: I developed this in python3 so make sure you are using that!
Now, if all went well, the app should be running on port 8000 in your web browser. Load the page http://127.0.0.1:8000/yoga/ in your browser. Now, at this point, nothing will be displayed. Instead, you will be prompted for input at the terminal pertaining to how you want the app to be personalized. The first question will ask you what type of class you want-- if you specify restorative, then you will only get easy postures, for example. The second question is how many poses you want. I would recommend 5-10 for restorative and 12-20 for regular vinyasa. Upon typing this, you will see the sequence in your browser! Simply reload the page to get a new sequence, and hit ctrl-c when you want to stop running the app.

The subfolder containing all the images I used is in the static folder inside of yoga_markov/yoga/static. These were all pulled from [this site](https://www.tummee.com/yoga/poses/all)

## Works Cited

- I learned Django from [this tutorial]
(https://docs.djangoproject.com/en/3.1/intro/tutorial02/), which I used as a template. I downloaded the django module and followed the steps to create the app using their sample app.
- I used [this article]
(https://www.freecodecamp.org/news/how-to-create-an-image-gallery-with-css-grid-e0f0fd666a5c/) to learn how to make the grid of images in CSS.
- I used [this article](
https://medium.com/@__amol__/markov-chains-with-python-1109663f3678) to use as an example of how to make a markov chain. I really didn't end up taking much code, but I used the general structure for my MarkovChain class.
- I used w3 schools to help with html/css stuff, [here](https://www.w3schools.com/cssref/pr_padding.asp)
