BEGIN{
    header = 0
}
{
    # убрать >
    if(/>/)
        gsub(/>/,"")
    # убрать возврат каретки
    if(/\r/)
        gsub(/\r/,"")

    # убрать пустые строки
    if (length() < 5)
        next

    # строки с именами столбцов
    if(/\[J/){
        sub(/\[J/," ")
        sub($1,"")
    }
    if(/No./)
    {
        sub(/. /," ")
        if (header == 1)
            next
        else
            header = 1
        # удалить все такие строки кроме самой перовй
    }

    print $0
}
END{
}
