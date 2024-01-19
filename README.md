To run this application, you need Python and AWS CLI credentials set up. Follow these steps to create a virtual environment and install the necessary packages:


**Create and Activate Virtual Environment:**

Run the following command to create a virtual environment (replace myenv with your desired environment name):

```bash
python -m venv myenv
```

Activate the virtual environment:
On Unix or MacOS, use:

```bash
source myenv/bin/activate
```

On Windows, use:

```bash
myenv\Scripts\activate
```

**Install Required Packages:**


- Clone the project repository from GitHub.
- Navigate to the project folder (where requirements.txt is located).
- Install the required packages by running:
```bash
pip install -r requirements.txt
```

**Configure AWS CLI:**

Ensure the AWS CLI is installed on your system. If not, download and install it from the official AWS CLI website. Configure your AWS credentials by running:
```bash
aws configure
```
Follow the prompts to enter your AWS Access Key ID, Secret Access Key, and default region.
