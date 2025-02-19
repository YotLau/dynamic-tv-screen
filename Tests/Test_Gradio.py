from gradio_client import Client


client = Client("stabilityai/stable-diffusion-3.5-large-turbo")
result = client.predict(
		prompt="A realistic tropical sunset over a calm ocean, with subtle colors of soft orange, pink, and blue hues blending into the sky. gentle waves, swaying palm trees, a smooth sandy beach, and a few seagulls gliding in the distance, creating a tropical and exotic atmosphere",
		negative_prompt="",
		seed=0,
		randomize_seed=True,
		width=1792,
		height=1024,
		guidance_scale=0,
		num_inference_steps=10,
		api_name="/infer"
)
print(result)