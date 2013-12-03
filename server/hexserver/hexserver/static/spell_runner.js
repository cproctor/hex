
// Expects underscore and Raphael.js

var SpellRunner = function(selector) {
    this.init(selector)
}

SpellRunner.prototype = {

    init: function(selector) {
        this.selector = selector
    },

    drawHex: function() {
        this.paper = Raphael(320,20,400,400)
        this.bulbs = []
        _.each(_.range(37), function(bulbNumber) {
            var coords = this.hexToCart(this.constants.bulbCoords[bulbNumber], this.constants.spacing)
            var circle = this.paper.circle(200 + coords[0], 200 + coords[1], this.constants.radius)
            circle.attr("fill", "r#f00-#fff")
            circle.attr("stroke", "#fff")
            circle.attr("strok-opacity", 0)
            this.bulbs.push(circle)
        }, this)
    },

    // runner.runSpell([[[[0,15,15],[36]]]], [[[[15,0,0], [30,31,32,33,34,35]]],[[[0,15,0], [30,31,32,33,34,35]]],[[[0,0,15], [30,31,32,33,34,35]]]], 4)
    runSpell: function(setup, loop, maxSeconds) {
        if (setup) {
            _.each(setup, function(frame, frameNum) {
                var runTime = frameNum * 1000 / this.constants.framesPerSecond
                if ( !maxSeconds || (runTime < maxSeconds * 1000))
                    setTimeout(_.bind(function() {this.applyFrame(frame)}, this), runTime)
            }, this)
        }
        setupTime = setup ? setup.length * 1000 / this.constants.framesPerSecond : 0
        if (loop) {
            console.log(loop)
            var loopFrame = 0
            this.loopIntervalId = setInterval(_.bind(function() {
                this.applyFrame(loop[loopFrame % loop.length])
                if (maxSeconds && (loopFrame * 1000 / this.constants.framesPerSecond + setupTime >= maxSeconds * 1000))
                    this.clearLoopInterval()
                loopFrame += 1
            }, this), 1000 / this.constants.framesPerSecond)
        }
    },

    clearLoopInterval: function() {
        clearInterval(this.loopIntervalId)
    },

    applyFrame: function(frame) {
        _.each(frame, function(layer) {
            this.applyLayer(layer)
        }, this)
    },

    applyLayer: function(layer) {
        var fill = "r" + this.rgbToHex(layer[0].slice(0,3)) + "-#fff"
        _.each(layer[1], function(bulbNum) {
            this.bulbs[bulbNum].attr('fill', fill)
        }, this)
    },

    rgbToHex: function(rgbColor) {
        return _.reduce(rgbColor, function(memo, colorValue) {
            return memo + colorValue.toString(16)
        }, '#')
    }, 

    hexToCart: function(hexCoords, scale) {
        scale = scale ? scale : 1
        var matrix = [[3/2, -1], [3/2, 1], [0, Math.sqrt(3)]]
        return _.map([0,1], function(cartCoord) {
            return scale * _.reduce(hexCoords, function(memo, hexCoord, i) {
                return memo + hexCoord * matrix[i][cartCoord]
            }, 0)
        })
    },
        
    constants: {
        spacing: 28,
        radius: 24,
        framesPerSecond: 24,
        bulbCoords: {
            0   : [0, 3, 0],
            1   : [0, 2, 1],
            2   : [0, 1, 2],
            3   : [0, 0, 3],
            4   : [-1, 0, 2],
            5   : [-2, 0, 1],
            6   : [-3, 0, 0],
            7   : [-2, -1, 0],
            8   : [-1, -2, 0],
            9   : [0, -3, 0],
            10  : [0, -2, -1],
            11  : [0, -1, -2],
            12  : [0, 0, -3],
            13  : [1, 0, -2],
            14  : [2, 0, -1],
            15  : [3, 0, 0],
            16  : [2, 1, 0],
            17  : [1, 2, 0],
            18  : [0, 2, 0],
            19  : [0, 1, 1],
            20  : [0, 0, 2],
            21  : [-1, 0, 1],
            22  : [-2, 0, 0],
            23  : [-1, -1, 0],
            24  : [0, -2, 0],
            25  : [0, -1, -1],
            26  : [0, 0, -2],
            27  : [1, 0, -1],
            28  : [2, 0, 0],
            29  : [1, 1, 0],
            30  : [0, 1, 0],
            31  : [0, 0, 1],
            32  : [-1, 0, 0],
            33  : [0, -1, 0],
            34  : [0, 0, -1],
            35  : [1, 0, 0],
            36  : [0, 0, 0]
        }
    },


}
