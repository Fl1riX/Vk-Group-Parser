import vk_api
from datetime import datetime

access_token = 'token'
api_version = '5.131'  

def parsing():
    try:
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()

        group = 'group'

        group_info = vk.groups.getById(group_id=group, v=api_version)
        group_id = group_info[0]['id']

        wall_posts = vk.wall.get(owner_id=-group_id, count=100, v=api_version)

        first_post_date = wall_posts['items'][-1]['date']
        last_post_date = wall_posts['items'][0]['date']

        first_post_date_dt = datetime.utcfromtimestamp(first_post_date)
        last_post_date_dt = datetime.utcfromtimestamp(last_post_date)

        formatted_first_post_date = first_post_date_dt.strftime('%Y-%m-%d %H-%M-%S')
        formatted_last_post_date = last_post_date_dt.strftime('%Y-%m-%d %H-%M-%S')

        file_name = f"path/{formatted_first_post_date} - {formatted_last_post_date}.txt"

        with open(file_name, 'a', encoding='UTF-8') as file:
            file.write(f"\n\n----Информация--из--группы--https://vk.com/{group}----\n\n")

        for post in wall_posts['items']:
            post_id = post['id']
            post_date = post['date']

            post_date_dt = datetime.utcfromtimestamp(post_date)
            formatted_post_date = post_date_dt.strftime('%Y-%m-%d %H:%M:%S')

            comments_offset = 0
            comments_count = 100

            while True:
                comments = vk.wall.getComments(owner_id=-group_id, post_id=post_id, v=api_version, count=comments_count, offset=comments_offset)

                if not comments['items']:
                    break
                
                with open(file_name, 'a', encoding='UTF-8') as file:
                    file.write(f"\n----Дата--создания--поста--{formatted_post_date}----\n\n")

                    for com_text in comments['items']:
                        file.write(com_text['text'] + '\n')

                comments_offset += comments_count
    except Exception as e:
        print(e)

if __name__ == '__main__':
    parsing()
