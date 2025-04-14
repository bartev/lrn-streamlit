"""
Author: Bartev
Date: 2025-04-13

Display color swatches

a clean and interactive Streamlit app that displays color swatches from:
* Matplotlib (CSS4_COLORS)
* Plotly (plotly.express.colors.qualitative)
* Tableau (via Plotly)
* Plotly Continuous Scales (as gradient bars)

You can browse, filter, and preview colors all in one place.

To run:
> streamlit run color_swatch_app.py
"""

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from matplotlib import cm
from plotly import express as px

# ---------- Function definitions


matplotlib_categorical_maps = [
    "tab10",
    "tab20",
    "tab20b",
    "tab20c",
    "Pastel1",
    "Pastel2",
    "Paired",
    "Set1",
    "Set2",
    "Set3",
    "Accent",
    "Dark2",
]


def get_mpl_colors(name, n_colors=12):
    cmap = cm.get_cmap(name)
    if hasattr(cmap, "colors"):
        # Use the actual color list for categorical colormaps
        colors = cmap.colors
    else:
        # Fallback for continuous colormaps
        colors = [cmap(i / (n_colors - 1)) for i in range(n_colors)]

    return [mcolors.to_hex(c) for c in colors[:n_colors]]


# From the maptplotlib documentation
# https://matplotlib.org/stable/users/explain/colors/colormaps.html
cmaps = {}
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(category, cmap_list):
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh, left=0.2, right=0.99)
    axs[0].set_title(f"{category} colormaps", fontsize=14)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect="auto", cmap=mpl.colormaps[name])
        ax.text(
            -0.01,
            0.5,
            name,
            va="center",
            ha="right",
            fontsize=10,
            transform=ax.transAxes,
        )

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    # Save colormap list for later.
    cmaps[category] = cmap_list
    st.markdown("https://matplotlib.org/stable/users/explain/colors/colormaps.html")
    return fig


def show_mpl_qualitative():
    """Show the mpl qualitative colormaps"""
    st.header("Matplotlib - Qualitative Palettes")
    fig = plot_color_gradients(
        "Qualitative",
        [
            "Pastel1",
            "Pastel2",
            "Paired",
            "Accent",
            "Dark2",
            "Set1",
            "Set2",
            "Set3",
            "tab10",
            "tab20",
            "tab20b",
            "tab20c",
        ],
    )
    st.pyplot(fig)


def show_mpl_plotly_qualitative():
    """Show Matplotlib qualitative colormaps with clickable hex values"""
    st.header("Matplotlib (Plotly) - Qualitative Palettes")

    for cmap_name in matplotlib_categorical_maps:
        colors = get_mpl_colors(cmap_name)
        df = pd.DataFrame({"Color": colors})

        st.subheader(cmap_name)

        # Display hex colors in a styled DataFrame
        st.dataframe(
            df.style.applymap(
                lambda c: (
                    f"background-color: {c}; color: white"
                    if c != "#FFFFFF"
                    else "color: black"
                )
            )
        )

        # Optional: Click-to-copy functionality using HTML
        st.markdown("Click a color below to copy its hex code:")
        color_boxes = "".join(
            f"""
            <div onclick="navigator.clipboard.writeText('{hex}')" 
                 style="display:inline-block; background:{hex}; 
                        width:80px; height:30px; line-height:30px; 
                        margin:4px; text-align:center; 
                        color: white; border-radius:4px; cursor:pointer;"
            >{hex}</div>
            """
            for hex in colors
        )
        st.markdown(color_boxes, unsafe_allow_html=True)


def show_mpl_plotly_1_line_qualitative():
    """Show Matplotlib qualitative colormaps using a compact Plotly plot with tooltips and copy support."""
    st.header("Matplotlib (Plotly 1 line)- Qualitative Palettes")

    fig = go.Figure()
    box_height = 30
    box_width = 30
    padding = 5

    for row, cmap_name in enumerate(matplotlib_categorical_maps):
        colors = get_mpl_colors(cmap_name)
        for col, color in enumerate(colors):
            fig.add_shape(
                type="rect",
                x0=col * (box_width + padding),
                x1=col * (box_width + padding) + box_width,
                y0=-row * (box_height + padding),
                y1=-row * (box_height + padding) + box_height,
                line=dict(width=1, color="white"),
                fillcolor=color,
            )
            fig.add_trace(
                go.Scatter(
                    x=[col * (box_width + padding) + box_width / 2],
                    y=[-row * (box_height + padding) + box_height / 2],
                    text=[color],
                    mode="markers",
                    marker=dict(size=box_width, color=color, opacity=0),
                    hovertemplate=f"{color}<extra>{cmap_name}</extra>",
                    name=cmap_name,
                    showlegend=False,
                )
            )
        # Add colormap name label
        fig.add_annotation(
            x=-10,
            y=-row * (box_height + padding) + box_height / 2,
            text=cmap_name,
            showarrow=False,
            xanchor="right",
            yanchor="middle",
            font=dict(size=12),
        )

    max_cols = max(len(get_mpl_colors(name)) for name in matplotlib_categorical_maps)
    fig.update_layout(
        width=max_cols * (box_width + padding) + 200,
        height=len(matplotlib_categorical_maps) * (box_height + padding) + 50,
        margin=dict(t=20, b=20, l=20, r=20),
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "💡 Hover a swatch to see the hex code. Copying on click not available yet here, but you can add it below or open a request!"
    )


def show_mpl_perceptually_uniform_sequential():
    """Show the mpl perceptually uniform sequential colormaps"""
    st.header("Matplotlib - Perceptually Uniform Sequential Colormaps")
    fig = plot_color_gradients(
        "Perceptually Uniform Sequential",
        ["viridis", "plasma", "inferno", "magma", "cividis"],
    )
    st.pyplot(fig)


def show_mpl_sequential():
    """Show the mpl sequential colormaps"""
    st.header("Matplotlib - Sequential Colormaps")
    fig = plot_color_gradients(
        "Sequential",
        [
            "Greys",
            "Purples",
            "Blues",
            "Greens",
            "Oranges",
            "Reds",
            "YlOrBr",
            "YlOrRd",
            "OrRd",
            "PuRd",
            "RdPu",
            "BuPu",
            "GnBu",
            "PuBu",
            "YlGnBu",
            "PuBuGn",
            "BuGn",
            "YlGn",
        ],
    )
    st.pyplot(fig)


def show_mpl_sequential_2():
    """Show the mpl perceptually uniform sequential colormaps"""
    st.header("Matplotlib - Sequential (2) Colormaps")
    fig = plot_color_gradients(
        "Sequential (2)",
        [
            "binary",
            "gist_yarg",
            "gist_gray",
            "gray",
            "bone",
            "pink",
            "spring",
            "summer",
            "autumn",
            "winter",
            "cool",
            "Wistia",
            "hot",
            "afmhot",
            "gist_heat",
            "copper",
        ],
    )
    st.pyplot(fig)


def show_mpl_diverging():
    """Show the mpl diverging colormaps"""
    st.header("Matplotlib - Diverging Colormaps")
    fig = plot_color_gradients(
        "Diverging",
        [
            "PiYG",
            "PRGn",
            "BrBG",
            "PuOr",
            "RdGy",
            "RdBu",
            "RdYlBu",
            "RdYlGn",
            "Spectral",
            "coolwarm",
            "bwr",
            "seismic",
            "berlin",
            "managua",
            "vanimo",
        ],
    )
    st.pyplot(fig)


def show_mpl_cyclic():
    """Show the mpl diverging colormaps"""
    st.header("Matplotlib - Cyclic Colormaps")
    fig = plot_color_gradients("Cyclic", ["twilight", "twilight_shifted", "hsv"])
    st.pyplot(fig)


def show_mpl_miscellaneous():
    """Show the mpl miscellaneous colormaps"""
    st.header("Matplotlib - Miscellaneous Colormaps")
    fig = plot_color_gradients(
        "Miscellaneous",
        [
            "flag",
            "prism",
            "ocean",
            "gist_earth",
            "terrain",
            "gist_stern",
            "gnuplot",
            "gnuplot2",
            "CMRmap",
            "cubehelix",
            "brg",
            "gist_rainbow",
            "rainbow",
            "jet",
            "turbo",
            "nipy_spectral",
            "gist_ncar",
        ],
    )
    st.pyplot(fig)


def show_mpl_css4_colors_with_filter():
    """Show all CSS4 Matplotlib colors, with optional filtering"""
    # --- Matplotlib CSS4 Colors ---
    st.header("Matplotlib - CSS4 Colors (filter)")

    mpl_colors = mcolors.CSS4_COLORS
    mpl_df = pd.DataFrame(list(mpl_colors.items()), columns=["Name", "Hex"])

    search = st.text_input("🔍 Filter matplotlib colors by name:", "")
    filtered_mpl = mpl_df[mpl_df["Name"].str.contains(search, case=False)]

    if filtered_mpl.empty:
        st.info("No colors match your search.")
    else:
        st.dataframe(
            filtered_mpl.style.applymap(
                lambda c: (
                    f"background-color: {c}; color: white"
                    if c != "#FFFFFF"
                    else "color: black"
                ),
                subset=["Hex"],
            )
        )


# --- Plotly ---


def plot_color_swatch(colors, title="Color Swatch"):
    fig = go.Figure()

    for i, color in enumerate(colors):
        fig.add_trace(
            go.Bar(
                x=[1],  # All bars same length
                y=[f"{i+1}"],  # Label by index
                orientation="h",
                marker=dict(color=color),
                showlegend=False,
                hoverinfo="none",
                text=color,
                textposition="inside",
                insidetextanchor="start",
                textfont=dict(color="white" if color.lower() != "#ffffff" else "black"),
            )
        )

    fig.update_layout(
        title=title,
        height=40 * len(colors),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    )
    return fig


def show_plotly_qual_swatches():
    """Show Plotly qualitative colors for a single palette"""

    # --- Plotly Qualitative Palettes ---
    st.header("Plotly - Qualitative Palettes")

    palette_names = [
        name
        for name in dir(px.colors.qualitative)
        if not name.startswith("_")
        and isinstance(getattr(px.colors.qualitative, name), list)
    ]

    selected_palette = st.selectbox("Choose a palette", palette_names)
    plotly_colors = getattr(px.colors.qualitative, selected_palette)
    # plotly_colors = px.colors.qualitative.__dict__[selected_palette]
    plotly_df = pd.DataFrame(
        {"Index": list(range(len(plotly_colors))), "Color": plotly_colors}
    )
    st.dataframe(
        plotly_df.style.applymap(
            lambda c: (
                f"background-color: {c}; color: white"
                if c != "#FFFFFF"
                else "color: black"
            ),
            subset=["Color"],
        )
    )
    st.plotly_chart(
        plot_color_swatch(plotly_colors, title=f"{selected_palette} Preview")
    )


def show_plotly_sequential_color_scales():
    """Show Plotly sequential color scales"""

    # --- Sequential Scales as Gradient Bars ---
    st.header("Plotly - Sequential Color Scales")

    seq_names = [
        name
        for name in dir(px.colors.sequential)
        if not name.startswith("_")
        and isinstance(getattr(px.colors.sequential, name), list)
    ]
    cont_palette = st.selectbox("Choose a sequential scale", seq_names)

    # gradient_colors = px.colors.sequential.__dict__[cont_palette]
    gradient_colors = getattr(px.colors.sequential, cont_palette)
    n_colors = len(gradient_colors)

    st.write(f"Gradient scale: {cont_palette} ({n_colors} colors)")

    gradient_html = f"""
    <div style="background: linear-gradient(to right, {', '.join(gradient_colors)});
                height: 40px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 10px;">
    </div>
    """
    st.markdown(gradient_html, unsafe_allow_html=True)
    st.plotly_chart(plot_color_swatch(gradient_colors, title=f"{cont_palette} Preview"))


def show_plotly_diverging_gradient_scales():
    """Show Plotly diverging color scales"""

    # --- Diverging Scales as Gradient Bars ---
    st.header("Plotly - Diverging Color Scales")
    div_names = [
        name
        for name in dir(px.colors.diverging)
        if not name.startswith("_")
        and isinstance(getattr(px.colors.diverging, name), list)
    ]

    div_palette = st.selectbox("Choose a diverging scale", div_names)

    # div_colors = px.colors.diverging.__dict__[div_palette]
    div_colors = getattr(px.colors.diverging, div_palette)
    n_colors = len(div_colors)

    st.write(f"Diverging scale: {div_palette} ({n_colors} colors)")

    diverging_html = f"""
    <div style="background: linear-gradient(to right, {', '.join(div_colors)});
                height: 40px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 10px;">
    </div>
    """
    st.markdown(diverging_html, unsafe_allow_html=True)
    st.plotly_chart(plot_color_swatch(div_colors, title=f"{div_palette} Preview"))


def plot_all_qualitative_palettes():
    fig = go.Figure()
    palette_names = [
        name
        for name in dir(px.colors.qualitative)
        if not name.startswith("_")
        and isinstance(getattr(px.colors.qualitative, name), list)
    ]

    cell_size = 20
    padding = 10

    for row, name in enumerate(palette_names):
        colors = getattr(px.colors.qualitative, name)
        for col, color in enumerate(colors):
            fig.add_shape(
                type="rect",
                x0=col * cell_size,
                x1=(col + 1) * cell_size,
                y0=-row * (cell_size + padding),
                y1=(-row + 1) * (cell_size + padding),
                line=dict(width=1, color="white"),
                fillcolor=color,
            )
        # Add the palette name on the left
        fig.add_annotation(
            x=-10,  # shift left
            y=-row * (cell_size + padding) + cell_size / 2,
            text=name,
            showarrow=False,
            xanchor="right",
            yanchor="middle",
            font=dict(size=12),
        )

    width = (
        max(len(getattr(px.colors.qualitative, name)) for name in palette_names)
        * cell_size
    )
    height = len(palette_names) * (cell_size + padding)

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        width=width + 150,
        height=height + 50,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
    )
    return fig

    st.header("Plotly - All Qualitative Palettes")
    st.plotly_chart(plot_all_qualitative_palettes(), use_container_width=True)


def main():
    st.set_page_config(layout="wide")
    st.title("🎨 Color Swatches Explorer")
    st.sidebar.title("🧭 Display Options")

    # Map of choice name to show, to function to run
    choice_map = {
        "Matplotlib - Qualitative Palettes": show_mpl_qualitative,
        "Matplotlib (Plotly) - Qualitative Palettes": show_mpl_plotly_qualitative,
        "Matplotlib (Plotly 1 line)- Qualitative Palettes": show_mpl_plotly_1_line_qualitative,
        "Matplotlib - CSS4 Colors (filter)": show_mpl_css4_colors_with_filter,
        "Matplotlib - Perceptually Uniform Sequential Colormaps": show_mpl_perceptually_uniform_sequential,
        "Matplotlib - Sequential Palettes": show_mpl_sequential,
        "Matplotlib - Sequential (2) Colormaps": show_mpl_sequential_2,
        "Matplotlib - Diverging Colormaps": show_mpl_diverging,
        "Matplotlib - Cyclic Colormaps": show_mpl_cyclic,
        "Matplotlib - Miscellaneous Colormaps": show_mpl_miscellaneous,
        "Plotly - Qualitative Palette": show_plotly_qual_swatches,
        "Plotly - Sequential Scales": show_plotly_sequential_color_scales,
        "Plotly - Diverging Scales": show_plotly_diverging_gradient_scales,
    }

    sections_to_show = st.sidebar.multiselect(
        label="Choose which color sections to show:",
        options=choice_map.keys(),
        default=[
            "Matplotlib - Qualitative Palettes",
            "Matplotlib (Plotly) - Qualitative Palettes",
            # "Matplotlib - CSS4 Colors (filter)",
            # "Plotly - Qualitative Palette",
        ],
    )

    for section in sections_to_show:
        # For each section, get the function and run it
        choice_map[section]()


if __name__ == "__main__":
    main()
