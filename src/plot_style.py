"""Estilo visual compartido por los gráficos de Biodata."""


def apply_figure_theme(figure, theme="dark"):
    """Armoniza una figura de Matplotlib con el tema activo."""

    if theme == "light":
        figure_color = "#ffffff"
        axes_color = "#fbfdfc"
        text_color = "#1b2b21"
        grid_color = "#d7e1da"
        spine_color = "#c7d4cc"
    else:
        figure_color = "#111820"
        axes_color = "#111820"
        text_color = "#eaf2ed"
        grid_color = "#324039"
        spine_color = "#435149"

    figure.patch.set_facecolor(figure_color)

    for axes in figure.axes:
        axes.set_facecolor(axes_color)
        axes.tick_params(colors=text_color)
        axes.xaxis.label.set_color(text_color)
        axes.yaxis.label.set_color(text_color)
        axes.title.set_color(text_color)

        for spine in axes.spines.values():
            spine.set_color(spine_color)

        axes.grid(color=grid_color, alpha=0.32, linewidth=0.7)

    return figure
