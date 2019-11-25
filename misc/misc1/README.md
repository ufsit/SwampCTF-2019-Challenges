# [SwampCTF 2019 Miscellaneous] Needle-Eye's Apprentice

## Flavor Text

**Just as Needle-Eye was apprenticed to Ethereal, Vanishing-Point was apprenticed to Samet who, showed him the right path. Needle-Eye learned the transformation from 3 to 2, Vanishing-Point, from 2 to 1. Vanshing-Point's craft was perfected once he learned not to devote a disproportionate amount of attention to
some concepts at the expense of others. He followed the path laid out for him, always clockwise and ever deeper. This is one of Vanishing-Point's earliest masterworks, the first of the Dark Forest series, called Figure 1. A region.**

* Flag: `flag{C1x1n_L1us_B00k}`
* Expected difficulty: medium


## Description

Challenge string is contained in file quadt.out


The challenge is presented as a string of characters from the set

{ "(", ")", "0", "1", "," } that represent a quadtree.

## Challenge Solution

The challenge is solved by realizing that Samet and the string "devote a disproportionate amount of attention to some concepts at the expense of others"

The recursive nature of the representation is reinforced by the text's observation about the path "always clockwise. This tells the ordering of the quadrants in the traversal. They are upper left, upper right, lower right, then lower left. The phrase "ever deeper" addresses the recursive nature of the process.

Inspecting the string, one can see that it is not a full binary tree. At the outermost level, it has four comma-separated list elements. This continues for thelements until one reaches an element that is a single 0. That single 0 corresponds to a sequence of all zeros in the subimage to which it corresponds.

The code can be written in a variety of ways. I wrote the code to reconstruct the image in a way that mirrors the code that constructs it. It generates subimages corresponding to the four comma-separated elements recursively, eating up more of the string as it goes.  If one writes the pogram this way, the tricky part is that when concatenating the sub-images, if a sub-image is too small, it needs to be expanded by replicating its elements in both horizontal and vertical dimensions the number of times necessary to match its neighbors. One can write this code being cognizant of the max-depth of the tree and can generate images based one their depth in the tree. That requires two passes and I'm too lazy to think about that much code.

If I had more time, I should have made you a Jupyter notebook, but I would have had to learn how to use Jupyter.

My generator/solver script is temp.py in src.
It requires a boat-load of libraries, so I'm not sure you'll be able to run it.
I can definiely show you the running script at your leisure.


Write a complete and descriptive solution (a writeup) to your challenge here.
All challenges must be solvable by the challenge creator and at least one other person.
If you can't solve your own challenge, what hope do others have?

```
Use code blocks when necessary to illustrate your point
```

And `inline code` to highlight commands or variable names.
Link to outside resources [if necessary](https://wikipedia.org), but try to
keep your solution self-contained. Feel free to link to internal files and directories ([`attachments/`](attachments/)) using Markdown.

An organizer should be able to use any included solving scripts or your instructions to replicate your solution. If we cannot, we will kick the problem back to you for additional work.
