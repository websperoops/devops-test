{% extends "_layouts/loggedin.html" %}
{% load blocklight_tags %}
{% load static %}
{% block leftbar %}
{% get_social_navbar user %}
{% endblock %}
{% block content %}

    document.addEventListener("DOMContentLoaded",blocklight_tracker())


    //Master Tracker Function/////
    function blocklight_tracker(){
        //Set Global Function Variables////
        var pageBtns = {};
        var formElements = {};
        var pageImgs = {};
        var pageVideos = {}
        var currentPage = location.href;
        var comingFrom = document.referrer;
        console.log(comingFrom)

        //If Forms are on page, check details of Form Elements
        var formCheck = document.querySelectorAll("form")
        if(formCheck.length > 0){
        var formItems = ["input", "textarea","select"]
        formItems.forEach(function(elementType){
            saveFormElements(formElements, elementType);
        });
        }
        var pageInputs = formElements["input"]
        var pageTextAreas = formElements["textarea"]
        var pageSelects = formElements["select"]
        //Add Check to Buttons
        button_tracker(pageBtns);
        img_tracker(pageImgs);
        video_tracker(pageVideos)
        console.log(pageInputs+pageTextAreas)
        //Update JSON file every 2 seconds.//
 
        setInterval(function(){
            var json_export = "{% url 'user_tracker' %}" +
            "?current_page=" + currentPage +
            "?refferer=" + comingFrom +    
            "?buttons=" + pageBtns +
            "?page_inputs=" + pageInputs + 
            "?text_areas =" + pageTextAreas +
            "?select_boxes=" + pageSelects +
            "?imgs=" + pageImgs +
            "?videos=" + pageVideos;
        
        console.log(json_export.Current_Page)
        json_export = JSON.stringify(json_export);
        console.log(json_export)
        }, 2000)
    }

    //Monitor Buttons//
    function button_tracker(pageBtns){
        var buttonClick = document.querySelectorAll("button");
        buttonClick.forEach(function(elem){
            saveElement(pageBtns,elem.innerHTML);
        })
        buttonClick.forEach(function(elem){
            elem.addEventListener("mouseover", function(e){
                var buttonName = e.srcElement.innerHTML
                countAction(pageBtns,e.srcElement.innerHTML)
            })
        })
    }
    //Monitor Form Elements///
    function saveFormElements(formElements, elementType){
        var item = document.querySelectorAll(elementType);
        formElements[elementType];
        var elementTypeObject = {}
        item.forEach(function(elem){
            saveElement(elementTypeObject, elem.name);
        })
        formElements[elementType] = elementTypeObject;
        item.forEach(function(elem){
            elem.addEventListener("mouseover", function(e){
                countAction(formElements[elementType],e.srcElement.name)
            })
        })
    }
    //Monitor Images//
    function img_tracker(pageImgs){
        var img = document.querySelectorAll("img")
        img.forEach(function(elem){
            saveElement(pageImgs,elem.src)
        });
        img.forEach(function(elem){
            countHoverTime(elem, pageImgs, pageImgs[elem.src], elem.src)
        })
    }

    //Monitor Videos//
    function video_tracker(pageVideos){
        var video = document.querySelectorAll("iframe")
        console.log(video)
        video.forEach(function(elem){
            saveElement(pageVideos, elem.className)
        });
        video.forEach(function(elem){
            videoPlayTime(elem, pageVideos, pageVideos[elem.className], elem.className)
        })
    }

    //JSON Object Builder Functions//
    function saveElement(obj,node){
        key = node;
        obj[key] = 0
    }

    function countAction(obj,node){
        key = node;
        obj[key] = obj[key] + 1
    }

    function trackTime(){

    }
    //Count Time Spent Hoving Over Element
    function countHoverTime(elem, obj, count, attr){
        var timer = count;
        var counter = 0
        elem.addEventListener("mouseover",function(e){
            counter = setInterval(function(){
                timer++
            }, 1000);
        })           
        elem.addEventListener("mouseout",function(e){
            obj[attr] = timer;
            clearInterval(counter);
        })
    }

    //Record how long a video was played//
    function videoPlayTime(elem, obj, count, attr){
        var timer = 0
        var counter = 0
        elem.addEventListener("click",function(e){
            counter = setInterval(function(){
                timer++
                console.log(timer)
            }, 1000);
        })
        window.addEventListener("scroll",function(e){
            obj[attr] = timer;
            clearInterval(counter);
        })
    }

    //function to track how far user scrolled on page
    function amountscrolled(){
        function getDocHeight() {
        return Math.max(
            document.body.scrollHeight, 
            document.documentElement.scrollHeight,
            document.body.offsetHeight, 
            document.documentElement.offsetHeight,
            document.body.clientHeight, 
            document.documentElement.clientHeight
    )
}
        var winheight= window.innerHeight || (document.documentElement || document.body).clientHeight
        var docheight = getDocHeight()
        var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop
        var trackLength = docheight - winheight
        var pctScrolled = Math.floor(scrollTop/trackLength * 100) // gets percentage scrolled (ie: 80 or NaN if tracklength == 0)
        console.log(pctScrolled + '% scrolled')
    }
 
    window.addEventListener("scroll", function(){
        amountscrolled()
    }, false)
    
    

