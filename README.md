
# Crestron Home Assistant Integration

This custom integration allows Home Assistant to communicate with a Crestron Home system, enabling control of devices such as lights, shades, and thermostats.

## Features

- Discover and control Crestron shades
- Automatically updates device states
- Secure integration using an `authkey`

## Installation

1. **Download the Repository**: Clone or download this repository to your Home Assistant configuration folder.
   ```bash
   cd /config/custom_components
   git clone https://github.com/jeffreyyoung55/Home-Assistant-Crestron-4-API-Integration.git
   ```

2. **Install Dependencies**: Ensure the `requests` library is installed in your Home Assistant environment.
   ```bash
   pip install requests
   ```

3. **Configure Home Assistant**: Add the integration to your `configuration.yaml`:
   ```yaml
   crestron_controller:
     base_url: "http://192.168.0.2"
     initial_token: "YourInitialTokenHere"
   ```

4. **Restart Home Assistant**: Restart Home Assistant to load the new integration.

## Usage

1. **Access the Integration**: Go to **Configuration** > **Devices & Services** and find the Crestron integration.
2. **Control Devices**: Devices such as shades will appear in Home Assistant. You can control them from the UI.

## Troubleshooting

- **No Devices**: Ensure the `authkey` and `base_url` are correctly configured and valid.
- **Errors in Logs**: Check the Home Assistant logs for any error messages and ensure the integration files are placed correctly.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
