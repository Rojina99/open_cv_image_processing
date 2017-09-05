Image processing program.

	Input 
	-> Image with dots as shapes

	Output
       -> Image with continuous shapes

       -> Shape type of input
       
       -> Area and parameters like width, height, radius

Here, image_editor is the main class.

	It accepts arguments as 
                        --data_path -> 'data path for specific image'

                        --save_dir -> 'directory to save output  images'
                        
                        --save_image -> 'image name to be saved'

	i.e.

	python image_editor.py --data_path "D:/project/open_cv/data/images/inputs/green_circle.jpg" --save_dir "D:/projec/open_cv/data/save/images" --save_image "green_circle.jpg"

All the args parameters are optional, if not given default parameters will be used.    
The default save_dir is none.So, no image is saved if input argument is not provided.

