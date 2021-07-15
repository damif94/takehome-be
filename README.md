# Bungalow Take Home Project for Backend Developer Role

## About This Project
This is a Django based assignment. We have created a base project for you to work from. 
You are free to vary from our original base if you would like to. We provide it with the intention of providing 
a common base for all candidates to work from and to hopefully save you a bit of time. 

If you need an introduction to Django, their docs are an excellent place to start: https://docs.djangoproject.com/en/3.2

We encourage you to use the Django Rest Framework for developing your API. This is a framework that we use extensively 
at Bungalow, and it provides some nice functionality out of the box. https://www.django-rest-framework.org/

## What to Build
We would like you to build an API that can be used to query some information about houses.
Sample data is provided in the `sample-data` folder.
We have provided the stub for a Django command to import the data. Finish writing this code.
You should use Django's ORM to model the data and store it in a local database.
Then, utilize the Django Rest Framework to provide an API to query the models.
A very basic API design here would simply return all of the data available.
You can choose to improve and refine this very basic API design, and we encourage you to do so.
This will give us an opportunity to see how you approach API design.
If you are running out of time, you can outline how you would have done things differently given more time.


## How Will This Be Evaluated
We will use this project as our basis for our evaluation of your coding skill level as it relates to our team.
To do this, we will review your code with an eye for the following:

- Design Choices - choice of functionality, readability, maintainability, extendability, appropriate use of language/framework features
- Does it work as outlined
- Testing - have you considered how you'd test your code?
- Documentation - have you provided context around decisions and assumptions that you have made?
- Polish - have you produced something that would be ready to go into a production system?
  if not, have you clearly stated what would be needed to get from where it is to that level of polish?

## Time Expectations
We know you are busy and likely have other commitments in your life, so we don't want to take too much of your time.
We don't expect you to spend more than 2 hours working on this project. That being said, if you choose to put more or
less time into it for whatever reason, that is your choice. Feel free to indicate in your notes below if you worked on
this for a different amount of time and we will keep that in mind while evaluating the project. You can also provide us
with additional context if you would like to. Additionally, we have left a spot below for you to note. If you have ideas 
for pieces that you would have done differently or additional things you would have implemented if you had more time, 
you can indicate those in your notes below as well, and we will use those as part of the evaluation. For example, if you 
would have tested more, you can describe the tests that you would have written, and just provide 1 or 2 actual implemented
tests.

## Public Forks
We encourage you to try this project without looking at the solutions others may have posted. This will give the most
honest representation of your abilities and skills. However, we also recognize that day-to-day programming often involves 
looking at solutions others have provided and iterating on them. Being able to pick out the best parts and truly 
understand them well enough to make good choices about what to copy and what to pass on by is a skill in and of itself. 
As such, if you do end up referencing someone else's work and building upon it, we ask that you note that as a comment. 
Provide a link to the source so we can see the original work and any modifications that you chose to make. 

## Setup Instructions
1. Fork this repository and clone to your local environment. If you make your fork private, 
1. Install a version of Python 3 if you do not already have one. We recommend Python 3.8 or newer.
1. You can use the built-in virtual environment creation within Python to create a sandboxed set of package installs. 
   If you already have a preferred method of virtualenv creation, feel free to proceed with your own method. 
   `python -m venv env`    
1. You will need to activate your virtual environment each time you want to work on your project. 
   Run the `activate` script within the `env/bin` folder that was generated.
1. We have provided a `requirements.txt` file you can use to install the necessary packages.
   With your virtualenv activated run: `pip install -r requirements.txt`
1. To run the django server run `python manage.py runserver`
1. To run the data import command run `python manage.py import_house_data`
1. You are now setup and ready to start coding. 


# Your Notes

### Features
This feature consists of a GET endpoint which allows to list all the data provided from the csv,
with the posibility of adding filter parameters as `GET` parameters for restricting the data set
in a convenient way.

* `zillow_price__lt` and `zillow_price__gt` params allow you to filter houses based on the average zillow price
* `state` allows filtering on the US state the house is in
* `home__size__lt` and `home__size__gt` params for filtering on the home size.
* filter for exact matches on `n_bedrooms` and `n_bathrooms` for the number of bedrooms and bathrooms respectively.
* filter for `house_type` for exact match on house type.

### Design considerations:
- My first step was on deciding how the models would be (since this will have the most impact on other design decisions that come later).
  1.  I separated all the data from the csv into three models; `Home`, `Address` and `ZillowInfo`; plus two foreign keys; `zillow_info_fk`: `Home -> ZillowInfo`
      and `address_fk`: `Home -> Address`.
  1. `Home` will own all the fields that are intrinsic to the house (even if they were provided by Zillow), except the address.
  1. `Address` will collect zipcode, state, street and street number (this last two fields were a split from the `address` field in the csv: This model is 
     standalone and not part of the Home since it may come handy for other entities we may want to represent (thinking of renting whole buildings, 
     or knowing where our customers live for providing intelligent suggestions)
  1. `ZillowInfo` will encompass all zillow-specific data for the home they offer. If I understood well, Zillow is a real state marketplace; if we fetched their data for doing data analysis, 
     it is not hard to imagine we may want to rely on other sources. So a Home could be linked to many "data providers", appart from   Zillow.
* For the API, this time I decided to create a single GET endpoint which lists all the data fields using standard drf serializers with all the model fields. I also added [django-filters](https://github.com/carltongibson/django-filter/) 
   as a drf filter backend in order to provide GET lookup params which allow customized filtering on the GET endpoint. Here come some comments:
  1. I built the api using drf generics because it is easy to get this running, but I am aware that this is not generally suitable
    for projects in a mature stage (mostly to enable unsupported customizations).
  2. django-filters seems a good option when simple filters are needed, but the problem is that
     it would be nice that the api was flexible enough to select the fields it wants to fetch. Putting this all toghether,
     I think that a GraphQL based solution should do this job very well.
  3. Also, it could be necessary to add ordering specifications for the fetched data; even on multiple
     fields. That's why I added indexes on the models where ordering requirement seem plausible. For time limitations,
     I didn't add ordering capabilities to the django filter class.
    
### Testing
I didn't write tests this time, mainly because of time limitations. For this specific functionality and the way I 
wrote it (using out-of-the-box solution from trusted third-party packages like drf or django-filters), I may had put a focus on performance 
tests rather than functional tests.

I think it could be a good idea to add live performance monitoring (maybe with time threshold that trigger alarms) on the queries
duration. Even that we add performance tests, data in production may be different from that on QA and we could need to add
new indexes for boosting performance. 

It is also a possibility to use an indexation engine, like ElasticSearch;
which just would require to keep our data in sync with the one in there. There are some out-of-the-box solutions
for elasticsearch, like [Swiftype](https://swiftype.com/).

### Documentation
I added some docstrings for models with non-obvious purposes, and help_text for some of the fields.
I know that help_texts are intended for model forms, but I also find it handy for some cases (specifing
the measure unit of some field, e.g.).

In this case the requirements of the "feature" are fully described in the README; I like this approach.
Also, I normally link the issue to the jira/linear ticket for further referencing; mainly because non-technical employees
usually participate there and have no access to github.

### Anything else needed to make this production ready?
This is not ready for production. Here go the reasons:
1. No db configured. django default in-memory db most of the time is not even suitable for a dev environment 
   -as far as I recall, it even doesn't enforce pk and fk constraints-.
2. No authentication backend set. 
3. Even if this was an open api, we should put some throttling backend to defend from malicious boting which may
intend to leave our server sending 429's.
   

### Assumptions
*Did you find yourself needing to make assumptions to finish this?*

1. Maybe, I assumed that we where fetching zillow's data for doing automatic business analysis
which may help our company fix the prices for the homes we rent.

2. That this data endpoints will also be consumed by our web application, which may provide a detailed
search interface for our users.

*If so, what were they and how did they impact your design/code?*

1. On splitting the zillow csv in two models, one for the home intrinsic data and other for 
   zillow marketplace data. As I explained before, we could plug new data providers where we could
   be scrapping data from.
2. On deciding to allow filtering, and also on creating indexes for performant order-demanding queries.


### Next Steps
I think I cover this point all along the previous titles.  
Maybe I could add a more robust parser for the imprort_data which may expect nullables at every field. Same for ZillowInfo models.


### Time Spent
* I took 20 minutes for reasearch on django-filters, which I knew existed but had never used before.
* 20 minutes to analyze the data, understand each field; I had to visit Zillow to get more context.
* 3 hours for pure development and manual testing.
* 1.5 hours for the readme.



## How to Use
*Provide any end user documentation you think is necessary and useful here*

After following the instruction step 5, you should run the command 
`python manage.py makemigrations` 
which will create the data models in the django in-memory database.

You can then follow steps 6 and 7 and setup is complete.

You are ready to test the api using a curl example!

<img width="1667" alt="Screen Shot 2021-07-14 at 21 37 19" src="https://user-images.githubusercontent.com/29461526/125710402-162ba725-e397-42e3-b030-08bd3377aa8d.png">


