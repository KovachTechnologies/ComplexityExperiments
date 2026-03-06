#!/usr/bin/python

###########################################################################
#
# name          : complexity.py
#
# purpose       : complexity examples for book
#
# usage         : python complexity.py --<arg>
#
# description   :
# https://stackoverflow.com/questions/15024461/plot-mandelbrot-with-matplotlib-pyplot-numpy-python
# https://realpython.com/mandelbrot-set-python/
# https://stackoverflow.com/questions/12444716/how-do-i-set-the-figure-title-and-axes-labels-font-size
# https://stackoverflow.com/questions/6390393/how-to-change-tick-label-font-size
#
###########################################################################


import functools
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas
import random
import scipy as sp
import time


def mandelbrot1() :
    x, y = np.ogrid[-2:1:500j, -1.5:1.5:500j]

    iterations = 9

    c = x + 1j*y

    z = functools.reduce(lambda x, y: x**2 + c, [1] * iterations, c)

    plt.figure(figsize=(10, 10))
    plt.imshow(np.angle(z));
    plt.savefig( "graphs/madelbrot_angle.png", dpi=300 )


    plt.figure(figsize=(10, 10))
    plt.imshow(np.log(np.abs(z)));
    plt.savefig( "graphs/madelbrot_abs.png", dpi=300 )


def mandelbrot( threshold=2, iterations=500) :
    x,y=np.ogrid[-2:1:5000j,-1.5:1.5:5000j]

    c=x + 1j*y
    z=0
    for g in range( iterations ):
        print( f'Iteration number: {g}', end="\r")
        z = z**2 + c

    if threshold is None :
        plt.imshow(np.log(np.abs(z).T),extent=[-2,1,-1.5,1.5], interpolation='none')
    else :
        mask=np.abs(z) < threshold
        plt.imshow(mask.T,extent=[-2,1,-1.5,1.5])
        plt.gray()

    plt.ylabel( "Im(c)" )
    plt.xlabel( "Re(c)" )

    plt.savefig( "graphs/madelbrot.png", dpi=300 )


def mandelbrot_views( threshold=2, iterations=500 ) :
    with open( "mandelbrot_views.json", "r" ) as f :
        data = json.load( f )

    fig, axs = plt.subplots(2, 3)
    plt.gray()

    index = 1
    for ii in range( 2 ) : 
        for jj in range( 3 ) : 
            datum = data[ index ]
            xmin = datum[ "x" ][ 0 ]
            xmax = datum[ "x" ][ 1 ]
            ymin = datum[ "y" ][ 0 ]
            ymax = datum[ "y" ][ 1 ]

            x,y=np.ogrid[xmin:xmax:5000j,ymin:ymax:5000j]

            c=x + 1j*y
            z=0
            for g in range( iterations ):
                print( f'Iteration number: {index} {g}', end="\r")
                z = z**2 + c

            mask=np.abs(z) < threshold

            axs[ii, jj].imshow(mask.T,extent=[xmin,xmax,ymin,ymax])
            axs[ii, jj].set_title( datum[ "name" ], fontsize=4 )
            index += 1

            if index >= len( data ) :
                break

    for ax in axs.flat:
        ax.ticklabel_format(style='plain')
        ax.set_xlabel('Re(c)', fontsize=6 )
        ax.set_ylabel('Im(c)', fontsize=6 )
        ax.tick_params(axis='both', which='major', labelsize=4)
        ax.tick_params(axis='both', which='minor', labelsize=4)

    fig.tight_layout()
    plt.savefig( "graphs/madelbrot_views.png", dpi=300 )
    plt.close()

    

def mandelbrot_sequence( c=0, n=9 ):
    z = 0
    for i in range( n ) :
        yield z
        z = z ** 2 + c


def plot_mandelbrot_sequence( x=0, y=0, n=15 ) :
    data = [] 
    c = x + 1j*y
    output_filename =  f"{x}+{y}i.png" 
    output_title = f"c={x}+{y}i"
    print( output_filename.replace( ".png", "" ) ) 
    for i, v in enumerate( list( mandelbrot_sequence( c=c, n=n ) ) ) :
        if i != 0 :
            data.append( { "iteration" : i, "abs(z)" : np.abs(v) } )
        if np.abs( v ) > 10**8 :
            break
    json_filename = output_filename.replace( ".png", ".json" )
    json_filepath = os.path.join( "data", json_filename )
    with open( json_filepath, 'w' ) as f :
        json.dump( data, f, indent=2 )
    df = pandas.DataFrame( data )
    plt.plot( df[[ "iteration" ]], df[[ "abs(z)" ]], 'b' )
    plt.title( output_title, fontsize=14, loc='center')
    plt.ticklabel_format(style='plain')
    output_filepath = os.path.join( "graphs", "mandelbrot_sequences", output_filename )
    plt.savefig( output_filepath, dpi=300 )
    plt.close()


def mandelbrot_sequences() :
    print( "sequence1" )
    for i, v in enumerate( list( mandelbrot_sequence( c=1, n=9 ) ) ) :
        print( i, v )
    x = 1
    y = 0
    plot_mandelbrot_sequence( x=x, y=y )

    print( "sequence2" )
    for i, v in enumerate( list( mandelbrot_sequence( c=-1, n=9 ) ) ) :
        print( i, v )
    x = -1
    y = 0
    plot_mandelbrot_sequence( x=x, y=y )

    print( "sequence3" )
    x = 0.135
    y = 0.021
    c = x + 1j*y
    plot_mandelbrot_sequence( x=x, y=y )
    for i, v in enumerate( list( mandelbrot_sequence( c=c, n=9 ) ) ) :
        print( i, np.abs( v ) )

    for j in range( 10 ) :
        x = round( random.uniform( -1, 1 ), 3 )
        y = round( random.uniform( -1, 1 ), 3 )
        plot_mandelbrot_sequence( x=x, y=y )


def grid_plot_mandelbrot_sequences( n=15, bespoke_c=[] ) :
    fig, axs = plt.subplots(3, 3)

    index = 0
    for ii in range( 3 ) :
        for jj in range( 3 ) :
            if len( bespoke_c ) > 0 :
                x = bespoke_c[ index ][ 0 ]
                y = bespoke_c[ index ][ 1 ]
            else :
                x = round( random.uniform( -1, 1 ), 3 )
                y = round( random.uniform( -1, 1 ), 3 )

            if y < 0 :
                title =  f"{x}-{np.abs(y)}i" 
            else :
                title =  f"{x}+{y}i" 

            data = [] 
            c = x + 1j*y
            for i, v in enumerate( list( mandelbrot_sequence( c=c, n=n ) ) ) :
                if i != 0 :
                    data.append( { "iteration" : i, "abs(z)" : np.abs(v) } )
                if np.abs( v ) > 10**5 :
                    break

            df = pandas.DataFrame( data )
            axs[ii, jj].plot( df[[ "iteration" ]], df[[ "abs(z)" ]], 'b' )
            axs[ii, jj].set_title( title, fontsize=4 )
            index += 1

    for ax in axs.flat:
#        ax.ticklabel_format(useOffset=False) 
        ax.ticklabel_format(style='plain')
        ax.set_xlabel('iteration', fontsize=6 )
        ax.set_ylabel('abs(z)', fontsize=6 )
        ax.tick_params(axis='both', which='major', labelsize=4)
        ax.tick_params(axis='both', which='minor', labelsize=4)

    fig.tight_layout()

    # Hide x labels and tick labels for top plots and y ticks for right plots.
#    for ax in axs.flat:
#        ax.label_outer()

    t = time.time()
    output_filepath = os.path.join( "graphs", "mandelbrot_sequences_grid",  f"grid_mandlebrot_{t}.png" )
    plt.savefig( output_filepath, dpi=300 )
    plt.close()


def logistic_sequence( x=0, r=3.5, n=9 ):
    for i in range( n ) :
        yield x
        x = r * x * ( 1 - x ) 


def plot_logistic_sequence( x=0, r=3.5, n=15 ) :
    data = [] 
    output_filename =  f"r={r},x={x},n={n}.png" 
    output_title =  f"r={r}, x={x}.png" 
    print( output_filename.replace( ".png", "" ) ) 
    for i, v in enumerate( list( logistic_sequence( x=x, r=r, n=n ) ) ) :
        if i != 0 :
            data.append( { "iteration" : i, "X" : v } )
        if np.abs( v ) > 10**8 :
            break

    json_filename = output_filename.replace( ".png", ".json" )
    json_filepath = os.path.join( "data", json_filename )
    with open( json_filepath, 'w' ) as f :
        json.dump( data, f, indent=2 )
    df = pandas.DataFrame( data )
    plt.plot( df[[ "iteration" ]], df[[ "X" ]], 'b' )
    plt.title( output_title, fontsize=14, loc='center')
    output_filepath = os.path.join( "graphs", "logistic_sequences", output_filename )
    plt.savefig( output_filepath, dpi=300 )
    plt.close()


def logistic_sequences_r( x=0.5 ) :
    for i in range( 100 ) :
        r = 3 - ( float( i ) * 0.01 )
        plot_logistic_sequence( x=x, r=r, n=50 )

def logistic_sequences_x( r=3.6 ) :
    for i in range( 1, 99 ) :
        x = ( float( i ) * 0.01 )
        plot_logistic_sequence( x=x, r=r, n=50 )



def grid_plot_logistic_sequences(mode="x", X=0.5, R=3.735, n=50, bespoke_r=[], bespoke_x=[] ) :
    fig, axs = plt.subplots(3, 3)

    index = 0
    for ii in range( 3 ) :
        for jj in range( 3 ) :
            
            x = X
            r = R
            
            if mode == "r" :
                title_append = f"varying_r,x={x}"
                r = round( random.uniform( 2, 4 ), 3 )
            elif mode == "x" :
                title_append = f"varying_x,r={r}"
                x = round( random.uniform( 0, 1 ), 3 )
            elif mode == "bx" :
                title_append = f"bespoke_x={str(bespoke_x)},r={r}"
                x = bespoke_x[ index ]
            elif mode == "br" :
                title_append = f"bespoke_r={str(bespoke_r)},x={x}"
                r = bespoke_r[ index ]
            else :
                title_append = "varying_both"
                x = round( random.uniform( 0, 1 ), 3 )
                r = round( random.uniform( 2, 4 ), 3 )
            
            title =  f"x={x},r={r}" 

            data = [] 
            for i, v in enumerate( logistic_sequence( x=x, r=r, n=n ) ) :
                if i != 0 :
                    data.append( { "iteration" : i, "X" : np.abs(v) } )
                if np.abs( v ) > 10**8 :
                    break

            df = pandas.DataFrame( data )
            axs[ii, jj].plot( df[[ "iteration" ]], df[[ "X" ]], 'b' )
            axs[ii, jj].set_title( title, fontsize=4 )
            index += 1

    for ax in axs.flat:
#        ax.ticklabel_format(useOffset=False) 
        ax.ticklabel_format(style='plain')
        ax.set_xlabel('iteration', fontsize=6 )
        ax.set_ylabel('X', fontsize=6 )
        ax.tick_params(axis='both', which='major', labelsize=4)
        ax.tick_params(axis='both', which='minor', labelsize=4)

    fig.tight_layout()

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    output_filepath = os.path.join( "graphs", f"grid_logistic_{title_append}.png" )
    plt.savefig( output_filepath, dpi=300 )
    plt.close()


def grid_plot_similar_logistic_sequences() :
    plot_logistic_sequence( x=0.97, r=3.99, n=50 )
    plot_logistic_sequence( x=0.97001, r=3.99, n=50 )
    plot_logistic_sequence( x=0.97000001, r=3.99, n=50 )
    plot_logistic_sequence( x=0.98, r=3.99, n=50 )


def plot_logistic_pitchfork( x=0.5, n=1000, fineness=0.01, points_from=500, x1=1, x2=4 ) :
    results = []
    for r in np.arange( x1, x2, fineness ) :
        data = [ ( r, i ) for i in logistic_sequence( x=x, r=r, n=n ) ]
        results.extend( data[ 500 : ] )

    df = pandas.DataFrame( results )

    output_filepath = os.path.join( "graphs", f"logistic_pitchfork_x={x},n={n},fineness={fineness},x_in_[{x1},{x2}].png" )
    plt.scatter( df[[ 0 ]], df[[ 1 ]],  s=0.0001, color="black" )
    plt.savefig( output_filepath, dpi=900 )
    plt.close()

def do_logistic_pitchfork( x1, x2, fineness, n, x=0.5 ) :
    results = []
    for r in np.arange( x1, x2, fineness ) :
        data = [ ( r, i ) for i in logistic_sequence( x=x, r=r, n=n ) ]
        results.extend( data[ 500 : ] )
    return results

def plot_logistic_pitchforks() :
    x = 0.5
    n = 1500


    # logistic_pitchfork_x=0.5,n=1500,fineness=0.0001,x_in_[3.6276,3.8]
    ( x1, x2 ) = ( 3.6276,3.8 )
    title1=f"x1={x1},x2={x2}"
    fineness = 0.0003
    results = do_logistic_pitchfork( x1, x2, fineness, n )
    df1 = pandas.DataFrame( results )

    # logistic_pitchfork_x=0.5,n=1500,fineness=0.0001,x_in_[3.7389,3.9]
    ( x1, x2 ) = ( 3.7389,3.9 )
    title2=f"x1={x1},x2={x2}"
    fineness = 0.0003
    results = do_logistic_pitchfork( x1, x2, fineness, n )
    df2 = pandas.DataFrame( results )

    # logistic_pitchfork_x=0.5,n=1500,fineness=0.0001,x_in_[3.8284,4]
    ( x1, x2 ) = ( 3.8284,4 )
    title3=f"x1={x1},x2={x2}"
    fineness = 0.0003
    results = do_logistic_pitchfork( x1, x2, fineness, n )
    df3 = pandas.DataFrame( results )

    # logistic_pitchfork_x=0.5,n=1500,fineness=3e-05,x_in_[3.9601,4]
    ( x1, x2 ) = ( 3.9601, 4 )
    title4=f"x1={x1},x2={x2}"
    fineness = 0.00009
    results = do_logistic_pitchfork( x1, x2, fineness, n )
    df4 = pandas.DataFrame( results )

    df1.columns = [ "r", "x" ]
    df2.columns = [ "r", "x" ]
    df3.columns = [ "r", "x" ]
    df4.columns = [ "r", "x" ]

    fig, axs = plt.subplots(2, 2)

    axs[ 0, 0 ].scatter( df1[[ "r" ]], df1[[ "x" ]],  s=0.0001, color="black" )
    axs[ 0, 0 ].set_title( title1, fontsize=4 )
    axs[ 0, 1 ].scatter( df2[[ "r" ]], df2[[ "x" ]],  s=0.0001, color="black" )
    axs[ 0, 1 ].set_title( title2, fontsize=4 )
    axs[ 1, 0 ].scatter( df3[[ "r" ]], df3[[ "x" ]],  s=0.0001, color="black" )
    axs[ 1, 0 ].set_title( title3, fontsize=4 )
    axs[ 1, 1 ].scatter( df4[[ "r" ]], df4[[ "x" ]],  s=0.0001, color="black" )
    axs[ 1, 1 ].set_title( title4, fontsize=4 )

    for ax in axs.flat:
#        ax.ticklabel_format(useOffset=False) 
        ax.ticklabel_format(style='plain')
        ax.set_xlabel('r', fontsize=6 )
        ax.set_ylabel('x', fontsize=6 )
        ax.tick_params(axis='both', which='major', labelsize=4)
        ax.tick_params(axis='both', which='minor', labelsize=4)

    fig.tight_layout()

    # Hide x labels and tick labels for top plots and y ticks for right plots.
#    for ax in axs.flat:
#        ax.label_outer()

    output_filepath = os.path.join( "graphs", f"grid_logistic_pitchfork.png" )
    plt.savefig( output_filepath, dpi=300 )
    plt.close()


if __name__ == "__main__" :
    import argparse

    parser = argparse.ArgumentParser( description="Complexity Graphs" )

    # Add options for the different tasks
    parser.add_argument( '--mandelbrot-set', action='store_true', help="mandelbrot-set" )
    parser.add_argument( '--mandelbrot-views', action='store_true', help="mandelbrot-views" )
    parser.add_argument( '--mandelbrot-sequence', action='store_true', help="mandelbrot-sequence" )
    parser.add_argument( '--plot-mandelbrot-sequence', action='store_true', help="plot-mandelbrot-sequence" )
    parser.add_argument( '--grid-plot-mandelbrot-sequences', action='store_true', help="grid-plot-mandelbrot-sequences" )
    parser.add_argument( '--plot-logistic-sequence', action='store_true', help="plot-logistic-sequence" )
    parser.add_argument( '--grid-plot-logistic-sequences', action='store_true', help="grid-plot-logistic-sequences" )
    parser.add_argument( '--plot-logistic-pitchfork', action='store_true', help="plot-logistic-pitchfork" )
    parser.add_argument( '--vary-r', action='store_true', help="vary-r" )
    parser.add_argument( '--vary-x', action='store_true', help="vary-x" )
    parser.add_argument( '--vary-both', action='store_true', help="vary-both" )
    parser.add_argument( '--vary-bespoke-r', action='store_true', help="vary-bespoke-r" )
    parser.add_argument( '--vary-bespoke-x', action='store_true', help="vary-bespoke-x" )

    args = parser.parse_args()


    if args.mandelbrot_set :
        mandelbrot( threshold=2, iterations=500 )

    if args.mandelbrot_views :
        mandelbrot_views( threshold=2, iterations=50 )

    if args.mandelbrot_sequence :
        x = -0.239 
        y = 0.51
        c = x + 1j*y
        values = [ ( i, float( np.abs( v ) ) ) for i, v in enumerate( mandelbrot_sequence( c=c, n=20 ) ) ]
        output_filename = f"{x}+{y}i"
        print( json.dumps( values, indent=2 ) )
        output_filepath = os.path.join( "data", output_filename )
        with open( output_filepath, 'w' ) as f :
            json.dump( values, f, indent=2 )

    if args.plot_mandelbrot_sequence :
        x = -0.239
        y = 0.51
        plot_mandelbrot_sequence( x=x, y=y, n=50 )

    if args.grid_plot_mandelbrot_sequences :
        bespoke_c = [
            [ -0.482, -0.117],
            [ -0.697, -0.36],
            [ 0.25, -0.01 ],
            [ -0.737, 0.189 ],
            [ -0.125, 0.686 ],
            [ 0.026, -0.75 ],
            [ 0.29, 0.111 ],
            [ -0.887, 0.092 ],
            [ -0.635, 0.302 ]
        ]
        grid_plot_mandelbrot_sequences( n=50, bespoke_c=bespoke_c ) 

    if args.plot_logistic_sequence :
        plot_logistic_sequence( x=0, r=3.5, n=15 )

    if args.grid_plot_logistic_sequences :
        if args.vary_r :
            grid_plot_logistic_sequences( mode="r", X=0.5 )

        if args.vary_x :
            grid_plot_logistic_sequences( mode="x", R=3.99 )

        if args.vary_both :
            grid_plot_logistic_sequences( mode="rx" )

        if args.vary_bespoke_r :
            bespoke_r = [ 3 + i/10 for i in range( 9 ) ]
            grid_plot_logistic_sequences( mode="br" )

        if args.vary_bespoke_x :
            bespoke_x = [ 0.97 ]
            bespoke_x.extend( [ 0.97 + 0.01**(i + 1) for i in range( 8 ) ] )
#            for r in [ 3.8 + i/100 for i in range(20 ) ] :
#                grid_plot_logistic_sequences( R=r, n=100, mode="bx", bespoke_x=bespoke_x )
            r = 3.93
            grid_plot_logistic_sequences( R=r, n=100, mode="bx", bespoke_x=bespoke_x )

    if args.plot_logistic_pitchfork :
        plot_logistic_pitchfork( x=0.5, n=1500, fineness=0.001 )
