def get_segment_list(codes_from_csv, single_request_limit=100):
    """
    生成一个将所有的codes每100个分成一组的list
    Args:
      codes_from_csv: 从code.csv中读过来的所有codes
      single_request_limit: tushare.pro的每个request可包含的code数目的上限，目前是100

    Returns:
      一个将所有的codes每100个分成一组的list
    """
    segment_list = []
    code_list_length = len(codes_from_csv)
    for i in range(0, code_list_length, single_request_limit):
        start_index = i
        if i + 100 <= code_list_length:
            end_index = i + 100
        else:
            end_index = code_list_length
        segment_list.append("".join(codes_from_csv[start_index:end_index]).replace("\n", ","))
    return segment_list
