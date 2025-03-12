from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

image_name = "karol.jpg"                                     #zmienia nazwa pliku
image_location = "C:\karol"                                  #zmienia lokalizacje pliku
threshold=128                                                    #zmienia binaryzacje, mniej = wiecej bialego
full_path = os.path.join(image_location, image_name)
image = Image.open(full_path)
image.show()


def binarize_image(method='average'):
    global image, image_location, image_name, threshold


    if method == 'average':  #binaruzje srednia (?)
        grayscale_image = image.convert('L')
        grayscale_array = np.array(grayscale_image)
        binary_array = (grayscale_array > threshold) * 256
        result_image = Image.fromarray(binary_array.astype(np.uint8))
        file_name1=f"mono__{image_name}"
        new_file_path=os.path.join(image_location,file_name1)
        

    elif method in ['r', 'g', 'b']: #binaryzuje tylko red, green, blue
        rgb_image = image.convert('RGB')
        rgb_array = np.array(rgb_image)

        channel_index = {'r': 0, 'g': 1, 'b': 2}[method]
        channel_array = rgb_array[:, :, channel_index]
        binary_array = (channel_array > threshold) * 255
        result_image = Image.fromarray(binary_array.astype(np.uint8))
        file_name1=f"{method}__{image_name}"
        new_file_path=os.path.join(image_location,file_name1)

    else:
        raise ValueError(f"metody: 'average', 'r', 'g', 'b'")

    result_image.show()
    result_image.save(new_file_path)
    return result_image

binarize_image()
binarize_image('r')
binarize_image('g')
binarize_image('b')


def create_histogram(channel='all',show=True):
    global image, image_location, image_name
    
    figure, axis = plt.subplots(figsize=(10, 6))

    if channel == 'all':
        
        rgb_image = image.convert('RGB')
        rgb_array = np.array(rgb_image)


        colors = ['r', 'g', 'b']
        channel_names = ('Red', 'Green', 'Blue')

        for i, color in enumerate(colors):
            channel_data = rgb_array[:, :, i].flatten()
            axis.hist(channel_data, bins=256, range=(0, 255),
                    color=color, alpha=0.7, label=channel_names[i])

        axis.set_title('RGB Histogram')
        axis.legend()

    elif channel in ['r', 'g', 'b']:
        # Convert to RGB if not already
        rgb_image = image.convert('RGB')
        rgb_array = np.array(rgb_image)

        # Get specific channel
        channel_index = {'r': 0, 'g': 1, 'b': 2}[channel]
        channel_data = rgb_array[:, :, channel_index].flatten()

        # Plot histogram
        color_name = {'r': 'Red', 'g': 'Green', 'b': 'Blue'}[channel]
        axis.hist(channel_data, bins=256, range=(0, 255),
                color=channel, alpha=0.7, label=color_name)

        axis.set_title(f'{color_name} Channel Histogram')
        axis.legend()

    elif channel == 'average':
        # Convert to grayscale
        gray_image = image.convert('L')
        gray_array = np.array(gray_image).flatten()

        # Plot histogram
        axis.hist(gray_array, bins=256, range=(0, 255),
                color='gray', alpha=0.7, label='Grayscale')

        axis.set_title('Grayscale Histogram')
        axis.legend()

    # Set common properties
    axis.set_xlabel('Pixel Value')
    axis.set_ylabel('Frequency')
    axis.set_xlim([0, 255])
    axis.grid(True, alpha=0.3)

    # Save if path is provided

    plt.tight_layout()
    image_name1=f"histogram_{channel}_{image_name}"
    file_save_loc=os.path.join(image_location,image_name1)
    plt.savefig(file_save_loc)

    # Show if requested
    if show:
        plt.show()

    return figure, axis


create_histogram()
create_histogram('r')
create_histogram('g')
create_histogram('b')
create_histogram('average')
