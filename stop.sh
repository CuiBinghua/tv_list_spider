process_id=`ps aux | grep tv_list_spider.py | awk '{ print $2}'`
for i in $process_id
do
    echo "Kill tv_list_spider process [ $i ]"
    kill -9 $i
done

process_id=`ps aux | grep firefox | awk '{ print $2}'`
for i in $process_id
do
    echo "Kill firefox process [ $i ]"
    kill -9 $i
done