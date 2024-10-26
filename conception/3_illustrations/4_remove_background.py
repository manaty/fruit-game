
# Load the sixth image
image_path_son = '/icons/Son.png'
image_son = Image.open(image_path_son)

# Convert to RGBA to handle transparency
image_son = image_son.convert("RGBA")

# Get the image data as a numpy array
data_son = np.array(image_son)

# Replace white (or near white) with transparency
r, g, b, a = data_son.T
white_areas_son = (r > 200) & (g > 200) & (b > 200)
data_son[..., :-1][white_areas_son.T] = 0  # Set RGB to 0 for white areas
data_son[..., -1][white_areas_son.T] = 0  # Set alpha to 0 for transparency

# Create the output image for the sixth image
output_image_son = Image.fromarray(data_son)

# Save the output image
output_image_path_son = "/icons/Son_no_background.png"
output_image_son.save(output_image_path_son)

output_image_path_son

#then use gimp to fix the errors