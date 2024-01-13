"""make_surfaceを実行する際のパラメータ."""


class Param:
    """
    初期化用
    """
    """create_surface.py"""
    edit_normal = False
    show_vector26 = False
    work_create_process = False
    output_image = False
    point_only = False
    show_point = False
    show_normal = False
    show_mesh = False

    """edit_normal.py"""
    work_edit_process = False
    output_edit_image = False

    """
    以下切り替え用
    """

    """create_surface.py"""
    # 法線ベクトルの編集処理の有無
    edit_normal = True

    # 作業過程のグラフの表示
    # show_vector26 = True
    # work_create_process = True
    # output_image = True

    # meshなしplyファイルを作成するか
    # point_only = True

    # 法線ベクトルの表示
    # show_point = True

    # 法線ベクトルの表示
    # show_normal = True

    # meshの表示
    # show_mesh = True

    """edit_normal.py"""
    work_edit_process = True
    output_edit_image = True
