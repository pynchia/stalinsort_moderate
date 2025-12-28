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

        print(f"StalinSort\n {data=}\n {kept_elements=}\n {purged_elements=}")
        return kept_elements, purged_elements


class StalinSortModerated(StalinSort):
    def sort(self, data: list[int], order: SortOrder) -> list[int]:
        if not data:
            return []
        kept_elements, purged_elements = super().sort(data, order)  # apply StalinSort
        merged = self._merge(
            kept_elements,
            self.sort(purged_elements, order),  # the sorted purged elements
            order,
        )
        print(f"{merged=}")
        return merged
        
    @staticmethod
    def _merge(l1: list[int], l2: list[int], order: SortOrder):
        """
        Merge two sorted lists into one
        
        :param l1: the first sorted list
        :param l2: the second sorted list
        :param order: the order
        """
        operation = op.ge if order is SortOrder.asc else op.le
        merged_list = []
        from_list = iter(l1)
        to_list = iter(l2)
        if len(l1) > len(l2):
            from_list, to_list = to_list, from_list
        source_flag = 0  # fetch element from both
        while True:
            match source_flag:
                case 1:
                    try:
                        from_el = next(from_list)
                    except StopIteration:
                        merged_list.append(to_el)
                        return merged_list + list(to_list)
                case 2:
                    try:
                        to_el = next(to_list)
                    except StopIteration:
                        merged_list.append(from_el)
                        return merged_list + list(from_list)
                case _:  # fetch both
                    try:
                        from_el = next(from_list)
                    except StopIteration:
                        return merged_list + list(to_list)
                    try:
                        to_el = next(to_list)
                    except StopIteration:
                        return merged_list + list(from_list)

            if operation(from_el, to_el):
                merged_list.append(to_el)
                source_flag = 2
            else:
                merged_list.append(from_el)
                source_flag = 1


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

    sorted_data = StalinSortModerated().sort(data, sort_order)


    # for el in sorted_data:
    #     print(el)

    # kept_elements, purged_elements = StalinSort().sort(data, sort_order)
    # print(f"{data=}\n{kept_elements=}\n{purged_elements=}")

if __name__=="__main__":
    main()
