import numpy as np
from gca_rom import scaling


def save_error(error, norm, AE_Params, vars):
    """
    save_error(error: List[float], norm: List[float], AE_Params: object, vars: str)

    This function takes in two lists error and norm of same length and saves their relative error, along with the max, mean and min of the relative error to a txt file.

    The relative error is calculated as error/norm for each corresponding elements. The file is saved with a specific naming convention: AE_Params.net_dir + 'relative_errors' + AE_Params.net_run + vars + '.txt'

    Parameters:
    error (List[float]): A list of error values.
    norm (List[float]): A list of norm values of same length as error.
    AE_Params (object): An object containing information required to form the file name.
    vars (str): A string to be appended to the file name.
    """

    error = np.array(error)
    norm = np.array(norm)
    rel_error = error/norm
    np.savetxt(AE_Params.net_dir+'relative_errors'+AE_Params.net_run+vars+'.txt', [max(rel_error), sum(rel_error)/len(rel_error), min(rel_error)])


def print_error(error, norm, vars):
    """
    print_error(error: List[float], norm: List[float], vars: str)

    This function takes in two lists error and norm of same length and prints their absolute and relative errors, along with the max, mean and min of both the absolute and relative errors.

    The relative error is calculated as error/norm for each corresponding elements.

    Parameters:
    error (List[float]): A list of error values.
    norm (List[float]): A list of norm values of same length as error.
    vars (str): A string to describe the type of field.
    """

    error = np.array(error)
    norm = np.array(norm)
    rel_error = error/norm
    print("\nMaximum absolute error for field "+vars+" = ", max(error))
    print("Mean absolute error for field "+vars+" = ", sum(error)/len(error))
    print("Minimum absolute error for field "+vars+" = ", min(error))
    print("\nMaximum relative error for field "+vars+" = ", max(rel_error))
    print("Mean relative error for field "+vars+" = ", sum(rel_error)/len(rel_error))
    print("Minimum relative error for field "+vars+" = ", min(rel_error))


def compute_error(res, VAR, scaler, AE_Params):
    """
    Compute the absolute error and norm between the original data and the data generated by the autoencoder

    :param res: Resulting data generated by the autoencoder (numpy ndarray)
    :param VAR: Original data (numpy ndarray)
    :param scaler: Scaler object for scaling the data
    :param AE_Params: Autoencoder parameters (object)
    :return: error_abs_list, norm_z_list, lists of absolute error and norm for each snapshot of data
    """

    error_abs_list = list()
    norm_z_list = list()
    Z = scaling.inverse_scaling(VAR, scaler, AE_Params.scaling_type)
    Z_net = scaling.inverse_scaling(res, scaler, AE_Params.scaling_type)
    for snap in range(VAR.shape[0]):
        error_abs = np.linalg.norm(abs(Z[:, snap] - Z_net[:, snap]))
        norm_z = np.linalg.norm(Z[:, snap], 2)
        error_abs_list.append(error_abs)
        norm_z_list.append(norm_z)
    return error_abs_list, norm_z_list
