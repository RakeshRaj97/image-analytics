# image-analytics

This repository contains methods to perform image analytics on LinkedIn profile pictures

Following are the operations performed by taking a LinkedIn profile URL as an input,

1. Scrape the LinkedIn profile image URL from the input LinkedIN profile URL

2. Blur the background from the face  

3. Identify profiles where the face is at least 50-60% of the overall photo. If it's less than 50%, then score of face quality being too small  

4. Identify if teeth are visible. If so, mention teeth is shown  

5. Identity sentiment on face. E.g. smiling / happy, or neutral, sad.

6. Perform visual features recognition using Microsoft Computer Vision API.

Sample output:

![image](https://user-images.githubusercontent.com/47710229/87223338-6e9a5780-c3bf-11ea-947b-f5a8ee00e6ea.png)

