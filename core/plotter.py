#%% Imports 
import os
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
os.environ["PATH"] += os.pathsep + '/usr/local/texlive/2021/bin/universal-darwin'
plt.rcParams['font.family'] = 'Avenir'

#--Scripts

#%% Define a class for plotting useful 
class Plotter:
    def __init__(self):
        # To initialize the parameters 
        self.reset_params()
        # Create the output figures directory
        # If the figures folder does not exist, create it
        if not os.path.exists("figures"):
            os.makedirs("figures")

    def reset_params(self):
        #---colors
        self.color1 = '#1F77B4'
        self.color2 = '#FF7F0E'
        self.color3 = '#2CA02C'
        self.color4 = '#D62728'
        self.colors = [self.color1, self.color2, self.color3, self.color4]
        self.dot_color = self.color1
        #---a long list of matplotlib colors 
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        # Sort colors by hue, saturation, value and name.
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                        for name, color in colors.items())
        sorted_names = [name for hsv, name in by_hsv]
        self.color_list = sorted_names[:55:-1] # Remove all the dark colors and reverse the list
        #---labels
        self.x_label = "x"
        self.y_label = "y"
        #---figure size
        self.fig_size = (4,4)
        #---font sizes
        self.x_font_size = 16
        self.y_font_size = 16
        self.title_font_size = 20
        self.legend_font_size = 16
        self.x_tick_size = 14
        self.y_tick_size = 14
        #---line widths
        self.line_width = 2
        self.dash_width = 1
        #---border
        self.border_width_x_y = 2
        self.border_width_upper_right = 2
        #---ticks
        self.tick_width = 2
        self.tick_length = 6
        #---toggles
        self.show_plots = False
        self.log_scale_x = False
        self.log_scale_y = False
        #---text location
        self.text_loc = "upper left"
        #---pearson toggle
        self.pearson_toggle = True
        #---output png file name 
        self.png_name = "default.png"

    def set_text_loc(self, text_loc):
        if text_loc == "upper left":
            p_x = 0.05
            p_y = 0.90
            R_x = 0.05
            R_y = 0.80
        elif text_loc == "upper right":
            p_x = 0.50
            p_y = 0.90
            R_x = 0.50
            R_y = 0.80
        elif text_loc == "lower left":
            p_x = 0.05
            p_y = 0.20
            R_x = 0.05
            R_y = 0.10
        elif text_loc == "lower right":
            p_x = 0.50
            p_y = 0.20
            R_x = 0.50
            R_y = 0.10
        elif text_loc == "upper center":
            p_x = 0.30
            p_y = 0.90
            R_x = 0.30
            R_y = 0.80
        else:
            print("Invalid text location.")

        return p_x, p_y, R_x, R_y

    def polish_plot(self, output_PNG):
        # Set log scale if log_scale_x is True
        if self.log_scale_x:
            plt.xscale('log')
        # Set log scale if log_scale_y is True
        if self.log_scale_y:
            plt.yscale('log')

        # Increase tick font size
        plt.xticks(fontsize=self.x_tick_size)
        plt.yticks(fontsize=self.y_tick_size)

        # Increase the size of the ticks 
        plt.tick_params(axis='both', width=self.tick_width, length=self.tick_length)
        # Increase the size of the minor ticks
        plt.tick_params(axis='both', which='minor', width=self.tick_width/2, length=self.tick_length/2)

        # Increase the size of the border
        plt.gca().spines['top'].set_linewidth(self.border_width_upper_right)
        plt.gca().spines['right'].set_linewidth(self.border_width_upper_right)
        plt.gca().spines['bottom'].set_linewidth(self.border_width_x_y)
        plt.gca().spines['left'].set_linewidth(self.border_width_x_y)

        # Make the ticks point inwards
        plt.gca().tick_params(direction='in')
        # Make the minor ticks point inwards
        plt.gca().tick_params(which='minor', direction='in')

        # Tight layout
        plt.tight_layout()

        # Save figure
        plt.savefig("figures/" + output_PNG, dpi=800)

        # Show plot if show_plots is True
        if self.show_plots:
            plt.show()

    def default_negative_emotions(self, r_or_v, neg_emo, text_loc='upper left'):
        #---labels
        if r_or_v == 'return':
            self.x_label = "S&P500 mean return [basis points]"
        elif r_or_v == 'volume':
            self.x_label = "S&P500 mean volume [-]"
        else:
            raise "%s is not a valid input" % r_or_v
        self.y_label = r"Negative Emotions$_{%s}$ [-]" % neg_emo

        # Set the scatter plot color
        if neg_emo == '':
            self.dot_color = self.color1
        elif neg_emo == 'std':
            self.dot_color = self.color2
        elif neg_emo == 'pca':
            self.dot_color = self.color3
        elif neg_emo == 'dmd':
            self.dot_color = self.color4
        else:
            raise "%s is not a valid input" % neg_emo
        
        self.text_loc = text_loc

    def negative_emotions(self, df, x_key, y_key, png_fn=None):
        
        # Isolate the x and y variables
        x_orig = df[x_key].to_numpy()
        y = df[y_key].to_numpy()

        #--Plot the worths for each of the strategies
        # Set the figure size
        plt.figure(figsize=self.fig_size)

        #---Perform linear regression---#
        # Add constant to predictor variables
        x = sm.add_constant(x_orig)
        # Fit linear regression model
        model = sm.OLS(y, x).fit()
        # View model summary
        # print(model.summary())
        # Extract the Pearson correlation coefficient
        r = np.corrcoef(x[:,1],y)[0,1]
        # Add the p-value in the top left corner
        # Determine the x and y coordinates of the p-value and R^2 value
        p_x, p_y, R_x, R_y = self.set_text_loc(self.text_loc)
        p_str = '%.5f' % model.pvalues[1]
        # print the outputs
        print("corr coeff: ", r)
        print("p value   : ", p_str)
        # p_str = str(round(model.pvalues[1],3))
        plt.text(p_x, p_y,r'$p$' + ' = ' + p_str, fontsize=self.legend_font_size,transform=plt.gca().transAxes)
        # Add the r or R^2 value right below the p-value
        if self.pearson_toggle:
            r_str = '%.3f' % r
            plt.text(R_x, R_y,r'$r$' + ' = ' + r_str,fontsize=self.legend_font_size,transform=plt.gca().transAxes)
        else:
            R_squared_str = '%.3f' % model.rsquared
            plt.text(R_x, R_y,r'$R^2$' + ' = ' + R_squared_str,fontsize=self.legend_font_size,transform=plt.gca().transAxes)

        # Plot the fitted line
        plt.plot(x[:,1],model.fittedvalues, color='k', linewidth=self.line_width)

        # The y vs. x
        plt.scatter(x_orig, y, color=self.dot_color, linewidth=self.line_width)

        # Set the x and y labels
        plt.xlabel(self.x_label, fontsize=self.x_font_size)
        plt.ylabel(self.y_label, fontsize=self.y_font_size)

        # Make the plot better looking and save it
        if png_fn is not None: 
            self.polish_plot(png_fn)
        else:
            self.polish_plot(self.png_name)
