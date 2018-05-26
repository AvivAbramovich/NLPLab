def find_duration(driver):
    duration_div = driver.find_element_by_class_name('vjs-duration')

    duration_text = duration_div.text.strip()
    duration_arr = [int(d) for d in duration_text.split(':')]
    duration_arr.reverse()

    duration = duration_arr[0] + (60 * duration_arr[1])
    if len(duration_arr) > 2:
        duration += 3600 * duration_arr[2]

    if len(duration_arr) > 3:
        raise Exception('Unknown duration format "%s"' % duration_text)

    return duration
