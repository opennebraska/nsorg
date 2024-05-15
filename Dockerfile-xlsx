# https://stackoverflow.com/a/44350277/4656035
FROM python
RUN pip install "pandas[excel]"
RUN mkdir /home/report
RUN mkdir /home/data

# ARG src="OPS Referral Data 2018-2019.xlsx"
# COPY ${src} /home
COPY xlsx_to_sqlite.py /home
WORKDIR /home
CMD python /home/xlsx_to_sqlite.py

