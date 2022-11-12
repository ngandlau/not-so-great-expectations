from __future__ import annotations
from typing import Any, Dict, List,
import pandas as pd


class PandasExpectations(pd.DataFrame):
    """A wrapper for a pd.DataFrame that adds test methods.  
    This is along the lines of Great Expecations.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def from_pandas(cls, dataset: pd.DataFrame) -> PandasExpectations:
        """Creates a PandasExpectation-DataFrame from a pandas.DataFrame.
         
        Args:
            dataset (pd.DataFrame): A pandas DataFrame.
         
        Returns:
            PandasExpectations: A PandasExpectations DataFrame that has access to all expect_xyz methods.

        Example:
        ```
            df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            dfexpectations = PandasExpectations.from_pandas(df)
            dfexpectations.expect_colnames_to_be_in_list(colnames=['A','B'])
        ```
        """
        return cls(dataset)

    def expect_dataframe_to_have_columns(self, columns: List[str]) -> bool:
        """Checks if the dataframe has the columns specified in `columns`. Note
        that the dataframe *can* have more then the specified columns.
         
        Args:
            columns (List[str]): A list of column names that the dataframe should have.
         
        Returns:
            bool: True if the dataframe has all of the specified `columns`.
        """
        colnames_in_df = []
        colnames_not_in_df = []
        for colname in columns:
            if colname in self.colnames:
                colnames_in_df.append(colname)
            else:
                colnames_not_in_df.append(colname)
        
        if len(colnames_not_in_df) == 0:
            for colname in colnames_not_in_df:
                print(f"{colname} not included in {self.colnames}")
            return False
        else:
            return True

    def expect_columns_to_be_equal(self, columns: List[str]) -> bool:
        """Checks if the dataframe has exactly the columns specified in the list.
        The order of the column names in `columns` does not matter.
         
        Args:
            columns (List[str]): A list of column names.
         
        Returns:
            bool: #TODO
        """
        sorted_df_columns = sorted(self.columns)
        sorted_expected_columns = sorted(columns)

        if sorted_df_columns != sorted_expected_columns:
            if len(columns) != len(self.columns):
                print(f"The DataFrame has {len(self.columns)} but should have {len(columns)}.")
            missing_columns = [c for c in sorted_expected_columns if c not in sorted_df_columns]
            print(f"The DataFrame misses the following columns: {missing_columns}")
            return False
        else:
            return True

    def expect_schema_to_be_equal(self, expected_schema: Dict[str, Any]) -> bool:
        """Checks if the DataFrame has the expected schema. A schema is 
        a dictionary of {colname: dtype}.
         
        Args:
            expected_schema (Dict[str, Any]): A dictionary specifying the mapping colname -> dtype
         
        Returns:
            bool: _description_

        Example:
        ```
            from pandas import StringDtype

            df = pd.DataFrame({'str_column': ['hello', 'world'], 'int_column': [1, 2]})
            dfe = PandasExpectations.from_pandas(df)
            
            expected_schema = {'str_column': StringDtype, 'int_column': int}
            print(dfe.expect_schema_to_be_equal(expected_schema))
        ```
        """
        columns_have_correct_dtype = []
        for colname in expected_schema.keys():
            actual_dtype = self[colname].dtype
            target_dtype = expected_schema[colname]
            is_correct_dtype = actual_dtype == target_dtype
            if not is_correct_dtype:
                print(f"'{colname}' is of type {actual_dtype} but should be {target_dtype}")
            columns_have_correct_dtype.append(is_correct_dtype)
        return all(columns_have_correct_dtype)

    def expect_column_values_to_not_be_null(self, colname: str) -> bool:
        return all(self[colname].notnull())
    
    def expect_column_values_to_be_in_set(self, colname: str, set_: set) -> bool:
        value_is_in_set = []
        for value in self[colname].unique():
            if value in set_:
                value_is_in_set.append(True)
            else:
                print(f"{value} is not in {set_}")
                value_is_in_set.append(False)
        return all(value_is_in_set)

    def expect_column_values_to_be_a_subset_of(self, colname: str, superset: set[Any]) -> bool:
        values_not_in_superset = []
        for value in self[colname].unique():
            if value not in superset:
                values_not_in_superset.append(value)
        if len(values_not_in_superset) == 0:
            return True
        else:
            for value in values_not_in_superset:
                print(f"Value {value} is in column {colname} but it should not be.")
            return False
    
    def expect_column_values_to_not_be_in_set(self, colname: str, set_: set) -> bool:
        value_in_set = []
        for value in self[colname].unique():
            if value in set_:
                print(f"{value} is in {set_}")
                value_in_set.append(True)
            else:
                value_in_set.append(False)
        return not(any(value_in_set))

    def expect_column_mean_to_be_between(
        self, colname: str, strict_min: float, strict_max: float
    ) -> bool:
        mean = self[colname].mean()
        return strict_min <= mean <= strict_max


        

