# Bernhard Meeting Notes

## Issue
Issue is background just random noise, instead of occlusion or natural background using various elimination positions/light sources.

Problem with random background is need to adapt illumination to background. So from learning perspective random noise would have the same effect.

In real environments, overall lighting conditions have an effect. Model includes sampling of all conditions, sun positions, light positions etc. Illumination constant across the image.

Introducing wrong steep non-differential component.

But for this project too hard automatically to put background illumination (of stock photo) on foreground object.

## Suggested approach for basic proof of concept

Key Q: if just random noise: how good is if just one-class classifier. This would show general approach works. Can model identify in a random environment (e.g. warehouse). Is this better than just train on warehouse images?


If this works, then move to images taken kitchen. Naive, but sufficient comparison: compare our model with another model trained on warehouse images on test data on products in e.g. a kitchen. This would be our proof of concept.

For a basic approach, could even train from model gif on slack and see how it does (background not great and logo, but he thinks might not have terrible performance).

## Over-the-top approach
Model indoor scenes e.g. whole virtual environment of kitchen. Render product in model with lighting. Retracer (?), other sophisticated approaches.

Only extra thing you learn is to ignore clutter, but performance increases.

But an additional add-on - too much for main project component.

## Choice of background images
Issue: it will learn silhouettes where random images are outdoor images etc.

Issue is constant bias across the image.  We have different gradients.  

Possibility: ignore background by implement ignore component (-1 constant in architecture). But highly overfit on object as won't have other features.

He thinks random feature noise (across whole image or local features, which are just learned to be ignored) will perform fine.

If we have to pick image for background, use roads/grass because not as much illumination bias. Would have the bias in kitchen bedroom images. Maximum he would go to is kitchen background, with images/tests also on random background.

## Next steps for project
1. Train on random background.
  - Build a minimum pipeline and see if it trains at all.
  - Constant background or randomly changing. Tiling.
  - For constant background, he expects overfitting.
  - Validation set is synthetic images, test is warehouse.

2. Try warehouse image training and compare results.
3. Add features / improve
   - sim real environment
   - GAN
   - Backgrounds
   - Illumination (if focusses on product but can't identify the rendering or illumination)


Binary classification:
- Binary class first. Don't need more as can assume if it works on binary can work more more
- Can do more, but object or not is fine for first stage.
  - Should do one product vs no product. No product could be random or warehouse for other products. Doesn't matter.  
  - So we need a background class. For proof of concept can be product vs product, but ideal is representative background.


**But make sure we follow main path.**


## Data processing
Our main focus is: data acquisition + general augmentation approach. He expect us to be worse in warehouse but better on transferability.

The more data augmentation, the more invariant in data. Normally translation rotation flipping, which makes model ignore spacial distribution.

Risk overfitting as we have so many augmentation options. Constant background with light noise and blur might be enough.

### Model creation
Bottom of products:
Make sure hole not visible in training data. Just use slightly truncated hemispheres. Be very careful about the fillers in occluded side.

Artefacts on models:
See how much influence it has once we build the model. Might be worth mixing data: Ours + warehouse images. This would be a bit biased to warehouse environment but might be better than just using 3D model images. Lots of opportunity for experimentation! Tweak proportion.

Also add webshop to training.

### Approach
SO throw it all in but **keep focus on judging what variants/approaches actually contribute**

Other possible add on: can do some things on his light stage. Small single figure boost in final performance maybe.

Final conclusion for project: the approach works, but just needs more manpower.


## Keras/tenserflow

He doesn't mind. Can take foreign code or write your own.
Don't put too much work in architecture dev. Simple VGG would do fine if data is right. Mobile net might also be interesting.

Models are interchangeable. VGG/inception performance difference very small.

He like Keras for soft engine. Simplicity of testing.

Our project is 90% data management, evaluation, tweaking. maybe 10% coding architecture.

## Monday meeting
Monday meeting: brief explain approach.
