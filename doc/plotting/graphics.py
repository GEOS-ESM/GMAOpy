document(
    graphics = graphics(
        grid = False
    ),
    plot = [
        timeseriesplot(
            graphics = graphics(
                grid = True,
                linewidth = 3.0
            ),
            curve = [
                line(
                    graphics = graphics(
                        linewidth = 1.0
                    ),
                ),
                line(
                    graphics = graphics(
                        color = 'red'
                    ),
                )
            ]
        ),
        levelplot(
            graphics = graphics(
                alpha = 0.2
            )
        )
    ]
)
