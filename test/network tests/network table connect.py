import utils.net as cvnet


def main():
    vision_conn = cvnet.net_init(table_name='VisionTable')

    vision_conn.set("NTT", 666.0)

    import time
    time.sleep(0.5)

    # print vision_conn.get("robot x", "shit")


if __name__ == "__main__":
    main()
