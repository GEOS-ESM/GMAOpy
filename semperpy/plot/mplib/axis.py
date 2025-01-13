from semperpy.plot.graphics.attribute import Attribute

class Axis(Attribute):

    ticksize_ = ['','medium','small','x-small','xx-small'] + ['xx-small'] * 10

    def setHorizontal(self):
        self['horizontal'] = True

    def __call__(self,layout,subplot,labels=None,ticks=None,date=False,maj_locator=None,min_locator=None,formatter=None,rotation=None,tick_label_size=None,**kargs):
        self.overwrite_from(kargs)
        if 'rotation' in self:
            rotation = self['rotation']
        if 'min' in self or 'max' in self:
            self['auto_scale'] = False
        auto = self['auto_scale']
        min = self.get('min',0)
        if min is None:
            min = 0
        max = self.get('max',1)
        if max is None:
            max = 1.0
        if min == max:
            max = min + 1
        max = max * self['zoom']
        if self['horizontal']:
            if self['other_side']:
                subplot.xaxis.tick_top()
                subplot.xaxis.set_label_position("top")
            subplot.set_xlim(left=min,right=max,auto=auto)
            subplot.set_xscale(self['scale'])
            if labels is not None:
                if ticks is None:
                    ticks = list(range(len(labels)))
                subplot.set_xticks(ticks)
                subplot.set_xticklabels(labels)
            if date:
                subplot.xaxis_date()
            if maj_locator is not None:
                subplot.xaxis.set_major_locator(maj_locator)
            if min_locator is not None:
                subplot.xaxis.set_minor_locator(min_locator)
            if formatter is not None:
                subplot.xaxis.set_major_formatter(formatter)
            if rotation is not None:
                labels = subplot.get_xticklabels()
                i = 0
                for l in labels:
                    l.set_rotation(rotation)
                    l.set_horizontalalignment('right')
            ticks = subplot.get_xticklabels()
            if tick_label_size is None:
                if 'tick_label_size' in self:
                    tick_label_size = self['tick_label_size']
                    subplot.xaxis.get_offset_text().set_size(self['tick_label_size'])
                else:
                    tick_label_size = self.ticksize_[layout.cols_]
            for tick in ticks:
                tick.set_size(tick_label_size)
        else:
            if self['other_side']:
                subplot.yaxis.tick_right()
                subplot.yaxis.set_label_position("right")
            subplot.set_ylim(bottom=min,top=max,auto=auto)
            subplot.set_yscale(self['scale'])
            if labels is not None:
                if ticks is None:
                    ticks = list(range(len(labels)))
                ticks = list(range(len(labels)))
                subplot.set_yticks(ticks)
                subplot.set_yticklabels(labels)
            if date:
                subplot.yaxis_date()
            if maj_locator is not None:
                subplot.yaxis.set_major_locator(maj_locator)
            if min_locator is not None:
                subplot.yaxis.set_minor_locator(min_locator)
            if formatter is not None:
                subplot.yaxis.set_major_formatter(formatter)
            if rotation is not None:
                labels = subplot.get_yticklabels()
                for l in labels:
                    l.set_rotation(rotation)
            #ticks = subplot.get_yticklabels()
            if tick_label_size is None:
                if 'tick_label_size' in self:
                    tick_label_size = self['tick_label_size']
                    subplot.yaxis.get_offset_text().set_size(self['tick_label_size'])
                else:
                    tick_label_size = self.ticksize_[layout.cols_]
            subplot.margins(y = 0)
            #for tick in ticks:
            #    tick.set_size(tick_label_size)
        subplot.tick_params(direction='in', top=True, right=True, labelsize = tick_label_size)    

    def minmax(self,subplot):
        if self['horizontal']:
            return subplot.get_xlim()
        else:
            return subplot.get_ylim()

axis = Axis
