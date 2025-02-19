import os
import pickle
import click
import mlflow
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# mlflow.autolog()

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

@click.command()  # No change here
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):
    mlflow.autolog()  # No change here
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    rf = RandomForestRegressor(max_depth=10, random_state=0)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_val)

    rmse = mean_squared_error(y_val, y_pred, squared=False)
    mlflow.log_metric("validation_rmse", rmse)  # Change: Removed the extra space in the metric name

if __name__ == '__main__':
    import sys
    from click.testing import CliRunner

    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("trip-duration-experiment")
    with mlflow.start_run():
        runner = CliRunner()
        result = runner.invoke(run_train, sys.argv[1:])

        if result.exit_code != 0:
            raise Exception(f"Training failed: {result.output}")