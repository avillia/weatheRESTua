class PandasModelMixin:
    def as_dataframe_row(self, *args: str):
        dict_repr = self.__dict__.items()
        if args:
            return {key: value for key, value in dict_repr if key in args}
        return {
            key: value for key, value in dict_repr if key not in ("_sa_instance_state",)
        }
