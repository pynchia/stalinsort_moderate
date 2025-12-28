import enum
import operator as op
import pathlib
import sys


class SortOrder(enum.StrEnum):
    asc = "asc"
    desc = "desc"


class StalinSort:
    def sort(self, data: list[int], order: SortOrder) -> tuple[list[int], list[int]]:
        """
        StalinSort, i.e. purge the elements that are out of order
        
        :param data: the data to sort
        :param order: the order
        :return: a tuple of
            the numbers that are in order
            the purged numbers
        """
        operation = op.ge if order is SortOrder.asc else op.le
        kept_elements = []
        purged_elements = []
        prec_el = -1
        for curr_el in data:
            if operation(curr_el, prec_el):  # in order
                kept_elements.append(curr_el)
                prec_el = curr_el
            else:
                purged_elements.append(curr_el)

        return kept_elements, purged_elements


class StalinSortModerated(StalinSort):
    def sort(self, data: list[int], order: SortOrder) -> list[int]:
        kept_elements, purged_elements = super().sort(data, order)
        return 


def main():
    num_args = len(sys.argv) -1
    if  num_args < 1:
        print(f"usage: python {sys.argv[0]} DATAFILE_TO_SORT [asc/desc]")
        exit(-1)
    data_file = pathlib.Path(sys.argv[1])
    if not data_file.exists():
        print(f"Error: data file {sys.argv[1]} does not exist")
        exit(-2)
    sort_order = SortOrder(sys.argv[2]) if num_args == 2 else SortOrder.asc
    data = [int(line) for line in data_file.read_text().splitlines()]

    # sorted_data = StalinSortModerated().sort(data, sort_order)
    # for el in sorted_data:
    #     print(el)

    kept_elements, purged_elements = StalinSort().sort(data, sort_order)
    print(f"{kept_elements=}\n{purged_elements=}")

if __name__=="__main__":
    main()
