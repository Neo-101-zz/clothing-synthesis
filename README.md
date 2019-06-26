# Clothing Synthesis

Synthesize top image and bottom image into output image. 

## Input and Output

Every group of input consists of 4 input images.  

**input1.jpg:** top image  
**input2.jpg:** bottom image  
**input3.jpg:** match of top and bottom (wear top into bottom or not)  
**input4.jpg:** match of top and bottom (waer top into bottom or not)  
**output.jpg:** result of clothing synthesis

![overview](overview.png)

**NOTE:**  
This is just a picture to show groups of input and according output.  
The directory structure should be the same with this repository.  
Requirements of input images' name:  
**x**-input**y**.jpg  
**x** is the index of input group (starts from 1) and **y** is index of
particular input (1, 2, 3, 4).

## Dependencies Installation

To install the dependencies, navigate to the repository directory and
execute this command:

```bash
pip install -r requirements.txt
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
