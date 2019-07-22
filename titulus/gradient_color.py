import numpy as np
from IPython.core.display import display, HTML

def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
    return color_dict(RGB_list)

def color(toks, wgts, start_hex="#ffffff", finish_hex="#037ef3", middle_hex=None, n=20): #  # ff4c4c
    wgts = norm_wgts(wgts)
    wgts = get_wgts_cat(wgts, ncats=n)
    if not middle_hex:
        color_grad = linear_gradient(start_hex=start_hex, finish_hex=finish_hex, n=n)['hex']
    else:
        n_pos = int(n/2)
        n_neg = n - n_pos
        color_grad_pos = linear_gradient(start_hex=start_hex, finish_hex=middle_hex, n=n_pos)['hex']
        color_grad_neg = linear_gradient(start_hex=middle_hex, finish_hex=finish_hex, n=n_neg)['hex']
        color_grad = color_grad_neg + color_grad_pos
    return [color_token(t, color_grad[w]) for t, w in zip(toks, wgts)]

def norm_wgts(wgts):
    wgts_norm = wgts/np.linalg.norm(wgts, ord=2) # (wgts/np.sum(wgts, axis=-1, keepdims=True)).tolist()
    return wgts_norm

def get_wgts_cat(wgts, ncats):
    ncats_neg = min(int((ncats-1)/2), len([w for w in wgts if w<0]))
    ncats_pos = ncats - ncats_neg 
    min_wgts = np.min(wgts, axis=-1, keepdims=True)
    max_wgts = np.max(wgts, axis=-1, keepdims=True)
    wgts_cat_pos = np.array(wgts)*(ncats_pos-1)/(max_wgts+1e-10)
    wgts_cat_neg = np.array(wgts)*(ncats_neg+1)/(min_wgts+1e-10)
    wgts_cat = [ncats_neg + int(wgts_cat_pos[i]) if w>=0 else int(wgts_cat_neg[i]) for (i, w) in enumerate(wgts)]
    return np.asarray(wgts_cat)#.astype(int)

def color_token(text, background):
    return r'<div class="tag" style="background:'+background+';">'+text+'</div>'

def print_(text):
    return display(HTML("""
        <style>
        .tag {
         padding:2px 2px 2px 2px;
         border-radius: 5px 5px 5px 5px;
         overflow:hidden;
         display: inline-block;
        }
        </style>"""+text))