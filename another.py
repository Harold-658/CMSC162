from PIL import Image, ImageTk, ImageDraw #pip install pillow
import tkinter as tk #pip install tk
from tkinter.filedialog import askopenfilename

# This is the class constructor for the Image Processing App
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configures the app window
        self.title("Image Processor")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        
        # Gets the screen width and height
        screen_width = self.winfo_screenwidth() - 100
        screen_height = self.winfo_screenheight() - 100

        # Sets window size with screen dimension
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Configures the top bar of the App GUI
        self.topbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=1, relief="solid")
        self.topbar.grid(row=0, columnspan=3, sticky="ew") 
        
        # Configures the side bar of the App GUI
        self.sidebar = tk.Frame(self, width=100, bg="#2B2B2B")
        self.sidebar.grid(row=1, column=0, rowspan=4, sticky="nsew")
        
        # Configures the right side bar of the App GUI
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=2, sticky="nsew")
        
        # Configures the status bar of the App GUI
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=1, relief="solid")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        
        # Configures the Menu Bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Creates the File Menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # Adds menu items to the File menu
        file_menu.add_command(label='New')
        file_menu.add_command(label='Open...', command=self.open_img_file)
        file_menu.add_command(label='Open PCX...', command=self.open_pcx_file)
        file_menu.add_command(label='Close', command=self.close_img)
        file_menu.add_separator()

        # Adds Exit menu item
        file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        # Add the File menu to the menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )
        # Create the Help Menu
        help_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # Adds items on Help menu
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # Adds the Help menu to the menubar
        menubar.add_cascade(
            label="Help",
            menu=help_menu
        )
        
        # Configures the portion of the GUI where the image will reside
        self.image_label = tk.Label(self, bg="#242424")
        self.image_label.grid(row=1, column=1, sticky="nsew")
        
        # Configures open file button
        btn_open = tk.Button(self.sidebar, text="Open", command=self.open_pcx_file)
        btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
    # This is the function that opens the image file
    def open_img_file(self):
        filepath = askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.gif *.bmp *.jpeg *.tiff")])
        if not filepath:
            return
        
        image = Image.open(filepath)
        self.show_image(image)
        
    def show_image(self, image):
        # Opens the image using PIL
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()
        
        # Define the padding size
        padding_x = 20  # Horizontal padding
        padding_y = 20  # Vertical padding

        # Calculate the available space for the image within the label
        available_width = label_width - (2 * padding_x)
        available_height = label_height - (2 * padding_y)

        # Calculate the aspect ratio of the image
        aspect_ratio = image.width / image.height

        # Checks if the aspect ratio of the image is greater than the aspect ratio of the space available for the image to display
        if aspect_ratio > available_width/available_height:
            wpercent = available_width/float(image.width)
            hsize = int((image.height)*float(wpercent))
            image = image.resize((available_width, hsize))
        else:
            hpercent = available_height/float(image.height)
            wsize = int((image.width)*float(hpercent))
            image = image.resize((wsize, available_height))


        # Convert the PIL image to a PhotoImage object
        image_tk = ImageTk.PhotoImage(image)

        self.image_label.config(image=image_tk)
        self.image_label.image = image_tk  # Keep a reference to avoid garbage collection

        self.title(f"Image Viewer - {image}")
    
    def open_pcx_file(self):
        filepath = askopenfilename(filetypes=[("PCX Files", "*.pcx")])
        if not filepath:
            return
        
        with open(filepath, "rb") as file:
            # self.show_image(filepath)
            
            self.header = file.read(128)
            
            file.seek(0)
            size = len(file.read())
            print(f"adada: {size}")
            
            
            # pixel_data_size = file.seek(128,2) - 769
            # print(pixel_data_size)
            file.seek(128)
            image_data = file.read(size-128-768)
            
            file.seek(-768, 2)  # Go to the end of the file and move back 768 bytes
            color_data = file.read(768)
            
            i=0
            palette=[]
            
            while(i < len(color_data)):
                palette.append((color_data[i], color_data[i+1], color_data[i+2]))
                i += 3
            
            if self.header[0] != 10:
                raise ValueError("Not a valid PCX file.")
            else:
                content = file.read()
                #print(content)
                
                manufacturer = self.header[0]
                version = self.header[1]
                encoding = self.header[2]
                bits_per_pixel = self.header[3]
                x_min = self.header[4] + self.header[5] * 256
                y_min = self.header[6] + self.header[7] * 256
                x_max = self.header[8] + self.header[9] * 256
                y_max = self.header[10] + self.header[11] * 256
                
                width = x_max - x_min + 1
                height = y_max - y_min + 1
                print(f"{width}x{height}")
                
                hdpi = self.header[12]
                vdpi = self.header[14]
                nplanes = self.header[65]
                bytesperline = self.header[66] + self.header[67] * 256
                paletteinfo = self.header[68]
                
                pcx_image = self.decode(image_data)
                print(len(pcx_image))
                
                # Create a blank image with a white background
                img_pcx = Image.new('RGB', (width, height), (255, 255, 255))
                draw = ImageDraw.Draw(img_pcx)

                # Define the size of each color block
                block_size = 1

                # Draw the colored blocks on the image
                for i, color in enumerate(pcx_image):
                    if i%width == 0:
                        x1 = 0
                        y1 = i//width
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                    else:
                        x1 = (i%width) * block_size
                        y1 = (i//width) * block_size
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                        
                    draw.rectangle([x1, y1, x2, y2], fill=palette[color])
                    
                self.show_image(img_pcx)    
                
                # Create a blank image with a white background
                img_palette = Image.new('RGB', (256, 256), (255, 255, 255))
                draw = ImageDraw.Draw(img_palette)

                # Define the size of each color block
                block_size = 16

                # Draw the colored blocks on the image
                for i, color in enumerate(palette):
                    if i%16 == 0:
                        x1 = 0
                        y1 = i
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                    else:
                        x1 = (i%16) * block_size
                        y1 = (i//16) * block_size
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                        
                    draw.rectangle([x1, y1, x2, y2], fill=color)

                # Resize the image to 128x128
                img_palette = img_palette.resize((128, 128), Image.LANCZOS)

                # Convert the PIL image to a PhotoImage object
                image_tk_palette = ImageTk.PhotoImage(img_palette)

                # Create the canvas in the right sidebar
                self.create_right_sidebar_canvas()

                # Display the image on the canvas
                self.display_image_on_right_sidebar(image_tk_palette)

                # Add text to the canvas in the right sidebar
                self.add_text_to_right_sidebar(f"Manufacturer: {self.header[0]}", x=65, y=50, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Version: {self.header[1]}", x=44, y=70, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Resolution: {width} x {height}", x=86, y=90, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Encoding: {self.header[2]}", x=90, y=110, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Bits Per Pixel: {self.header[3]}", x=90, y=130, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"HDPI: {self.header[12]}", x=90, y=150, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"VDPI: {self.header[14]}", x=90, y=170, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Colormap: {self.header[16]}", x=90, y=190, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Number of Color Planes: {self.header[65]}", x=90, y=210, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Bytes Per Line: {self.header[66]}", x=90, y=230, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Palette Info: {self.header[68]}", x=90, y=250, fill="white", font=("Arial", 11))
    
    def decode(self, data):
        decoded_data = []
        i = 0
        
        while i < len(data):
            if data[i] >= 192:
                run_length = data[i] - 192
                pixel_value = data[i+1]
                decoded_data.extend([pixel_value]*run_length)
                i += 2
            else:
                decoded_data.append(data[i])
                i += 1
                
        return decoded_data

    def create_right_sidebar_canvas(self):
        # Create the canvas in the right sidebar
        self.canvas = tk.Canvas(self.rightsidebar, width=250, bg="#2B2B2B", highlightthickness=0)
        self.canvas.grid(row=1, column=2, sticky="nsew")

    def add_text_to_right_sidebar(self, text, x, y, fill, font):
        # Use the previously created canvas
        self.canvas.create_text(x, y, text=text, fill=fill, font=font)
    
    def display_image_on_right_sidebar(self, image_tk):
        canvas = tk.Canvas(self.rightsidebar, width=256, height=256, bg="#2B2B2B", highlightthickness=0)
        canvas.grid(row=5, column=2, sticky="nsew")

        # Create an image item on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        canvas.image = image_tk  # Keep a reference to avoid garbage collection
        
    def close_img(self):
        self.rightsidebar.destroy()
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=2, sticky="nsew")
        
        self.image_label.destroy()
        self.image_label = tk.Label(self, bg="#242424")
        self.image_label.grid(row=1, column=1, sticky="nsew")
                


if __name__ == "__main__":
    app = App()
    app.mainloop()
