# question1

Create a software API that gets log in information from users:

• if the information is correct, it directs them to the next page

• if the information is incorrect, it shows an error


If the user doesn’t have an account, it directs them to a page to create an account

• Get basic user information in that page, and create an account

Bonus point:
• Allow log in via gmail

# question2
1. Ask the user to upload some images with their text labels (e.g., an image of a cat,
an image of a dog, etc.)

2. Display one of the images to the user and ask the user to manually segment the
main object in the image (e.g., segment cat in the cat image); display the second
image and get its segmentation; save segmentation information

3. Add Gaussian noise (or other distortions) to images and repeat step 2

Bonus point:

• Use a classifier and get predicted labels for the images; display images (one by
one) along with output labels; ask the user if the predicted labels are correct
or not

• Compute the fraction of images the user thinks the labels were correct
