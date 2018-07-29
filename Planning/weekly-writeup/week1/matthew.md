# Week 1 Write-Up

## Matthew

### Items Completed This Week

#### Research

- Spatial Transformer Networks

  - During the course of my research into the topic, I came across the concept of Spatial Transformer Networks. This idea was developed at Google DeepMind, and are modules that can be added on to a standard CNN that aim to reduce its sensitivity to geometrical variance.
  - Given the huge amount of geometrical variance in the Ocado dataset (product are pictured at numerous angles and orientations), I realised that Spatial Transformer Networks could potentially be of great use to our project.
  - I also found a similar concept known as TI-Pooling, which seeks to achieve the same results in a slightly different way.
  - Reference paper: https://papers.nips.cc/paper/5854-spatial-transformer-networks.pdf
  - Spatial Transformer Networks tensorflow implementation: https://github.com/kevinzakka/spatial-transformer-network/blob/master/README.md
  - TI Pooling tensorflow implementation: https://github.com/dlaptev/TI-pooling

#### Experimentation, Coding and Implementation:

- Barcode scanning

  - We had previously hypothesised that automatically reading product barcodes where available might be a good way to increase accuracy and to provide an additional layer of confirmation.

  - I conducted some experiments to test this hypothesis. I tested barcodes from the Ocado dataset on various image barcode readers (specifically a few different python implementations on github, as well as a few commercial-grade solutions). Unfortunately, none of the barcode readers were successful in detecting/reading the Ocado barcodes (even though they were successful on other test images). I concluded that this was because the barcodes in the Ocado dataset were of very limited quality, due to the poor lighting conditions, low image resolution, and motion blur, making successful detection almost impossible.

- Text Recognition

  - We also hypothesised that reading the text on product labels might prove promising in providing additional confirmation of a product.

  - I conducted some experiments to test this hypothesis. Using Microsoft Azure's Text Recognition API, I was able to successfully read text from a test image. While the end-result was not perfect (a good number of characters were not read correctly), there were sufficient correctly read characters that one could reasonably see how this method might prove useful as a secondary means of confirming the validity of a product classification.

### Tasks for Next Week

#### Research

- Continue watching Stanford CS231n


#### Experimentation, Coding and Implementation:

- Make robotic turntable with Max
- Set up the Kinect to capture 3D models of objects placed on the turntable
- (If we manage to secure products) Begin making 3D models of our initial 10 products
- Complete initial report
- Max and I will assist the other pairs if we (hopefully!) don't encounter delays with implementing the 3D modelling system

### Time spent this week
- Research: 5 hours
- Experimentation: 2-3 hours

### Tasks on track?
- Yes
