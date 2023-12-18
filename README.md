# Markov Map Generator

## Introduction

My code generates a pixel art map using a Markov model. I intended for this to be a tool for creating fantasy worlds of some kind, such as for a written story, DND, or any other kind of fictional universe that someone might want to create. You could generate a map, come up with names for the various landmasses/bodies of water, and create a story yourself about the world. For example, if there were a mountain range separating two fields of grass, one could imagine that there is a town on either side who are completely isolated from each other. Or perhaps they eventually found a safe path through the mountains, and so they aren't separated anymore. Although I would argue that my code is not creative itself since it relies on set ratios of probabilities with no room for brand new land features (for example, it will never generate a new type of terrain or a new feature such as a volcano), it is meant to inspire creativity in others.

This system is meaningful to me because I could really benefit from a tool like this. There are tons of tips out there for world building on how to make a convincing map for a fantasy world, but none of them have really stuck for me. This system, however, can give the user more control over what kind of map they would like to generate (with some tweaking of the transition matrix). Even without modifying the code, this system provides where various features go. Many of the techniques I found for world-building just allowed for the creation of the outline of the landmasses, but didn't include any possibilities for saying where the mountains were, where deserts were, etc.

## Color key

Green = grass

Dark green = forest

Yellow = sand

Blue = water

Light gray = low mountain

Dark gray = high mountain

## How to run

You can run the main file normally, either through an IDE or the terminal. A file will be generated to the following path: "test_images/image.png" with the resulting image. If you want to keep this file, either rename it or move it elsewhere on your device. Otherwise, the file will be rewritten next time the program is run.

## The future

I would have liked to have made the outputs resemble real maps more. The outputs are somewhat streaky and don't really resemble a real landscape. I'd also like to play with the transition matix/resolution more to make it a more accurate representation of a real map. Another idea I had would be to name various features (i.e., rivers, mountain ranges, lakes, deserts, etc.). This could also be done with a Markov chain, either by chaining syllables together or by chaining individual letters. I wanted to display the names of each feature over the feature itself, just like in a real map.
