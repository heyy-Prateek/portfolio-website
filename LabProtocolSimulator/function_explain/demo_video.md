# Demo Video Feature

The Demo Video feature provides educational video content showing actual laboratory procedures for each experiment. This allows students to observe proper techniques and equipment operation before working in the physical laboratory.

## Implementation Overview

The demo video system is structured to:
1. Organize videos by experiment category
2. Stream videos embedded within the application
3. Provide contextual information and explanations
4. Allow full-screen viewing for detailed observation

## Code Structure

The demo video feature is implemented in the `chemengsim/videos/` directory. The main module is typically `demo_videos.py` which contains the display functions.

```python
# Main entry point in app.py for the Demo Video feature
if view_mode == "Demo Video":
    if experiment != "Home":
        exp_num = int(experiment.split(".")[0])
        from chemengsim.videos import demo_videos
        demo_videos.display_demo_video(exp_names[exp_num])
    else:
        # Display video selection page
        st.title("Demonstration Videos")
        st.markdown("""
        Select an experiment from the sidebar to view its demonstration video.
        """)
```

## Demo Video Module Structure

The demo videos module follows this typical pattern:

```python
import streamlit as st
import os
from pathlib import Path

# Dictionary mapping experiment names to video details
VIDEO_SOURCES = {
    "batch_reactor": {
        "title": "Isothermal Batch Reactor Demonstration",
        "source": "https://youtu.be/example_video_id",
        "description": "Demonstration of a batch reactor experiment...",
    },
    "semi_batch_reactor": {
        "title": "Semi-Batch Reactor Operation",
        "source": "https://youtu.be/example_video_id2",
        "description": "Step-by-step guide to semi-batch reactor operation...",
    },
    # Additional videos...
}

def display_demo_video(experiment_name):
    """Display the demonstration video for the selected experiment"""
    if experiment_name in VIDEO_SOURCES:
        video_data = VIDEO_SOURCES[experiment_name]
        
        # Display video title
        st.title(video_data["title"])
        
        # Display video
        st.video(video_data["source"])
        
        # Display description and additional information
        st.markdown("## Video Description")
        st.markdown(video_data["description"])
        
        # Add supplementary materials if available
        if "additional_materials" in video_data:
            st.markdown("## Additional Resources")
            for resource in video_data["additional_materials"]:
                st.markdown(f"- [{resource['title']}]({resource['url']})")
    else:
        st.error(f"No demonstration video available for {experiment_name}")
```

## Video Implementation Options

The demo videos can be implemented in several ways:

### 1. YouTube Embedding

Most commonly, videos are hosted on YouTube and embedded using Streamlit's `st.video()` function:

```python
st.video("https://youtu.be/video_id")
```

### 2. Local Video Files

For offline use, videos can be stored locally in the project:

```python
# Path to video files relative to the application
video_path = os.path.join("assets", "videos", f"{experiment_name}.mp4")

# Display local video
if os.path.exists(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
```

### 3. Alternative Embedding

For platforms like Vimeo or specialized educational video platforms:

```python
st.markdown(f"""
<iframe
    src="https://player.vimeo.com/video/{vimeo_id}"
    width="700"
    height="400"
    frameborder="0"
    allow="autoplay; fullscreen"
    allowfullscreen>
</iframe>
""", unsafe_allow_html=True)
```

## Video Content Organization

Each video is typically structured to include:

1. **Introduction**: Overview of the experiment and its purpose
2. **Equipment Setup**: Demonstration of proper equipment assembly
3. **Procedure**: Step-by-step walkthrough of the experiment
4. **Data Collection**: Showing how to collect and record measurements
5. **Analysis**: Examples of data analysis and interpretation
6. **Safety Considerations**: Important safety procedures and precautions

## Dependencies

The Demo Video feature has minimal external dependencies compared to other features:

- **Streamlit**: For the UI components and video embedding (`st.video()`)
- **Python Standard Library**: For file path handling (`os`, `pathlib`)
- **Internet Connection**: For streaming videos from external platforms (YouTube/Vimeo)

No additional package installations are required beyond the core Streamlit library for basic functionality.

## Extending the Demo Video Feature

To add a new demonstration video:

1. Record and edit the video demonstration
2. Upload the video to a hosting platform or include it in the assets directory
3. Add the video details to the `VIDEO_SOURCES` dictionary
4. Update any supplementary materials or resources

This modular approach allows instructors to easily update or add new video content without changing the core application logic. 