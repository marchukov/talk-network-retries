RP = csvread('~/tmp/pyconcz2016-net-failures/naive_probe.csv');
RT = csvread('~/tmp/pyconcz2016-net-failures/naive_download.csv');

RJ = csvread('~/tmp/pyconcz2016-net-failures/naive_get_json.csv');

% MB total per each 0.1 sec interval
AP = accumarray(floor(RP(:,1) * 10) + 1, RP(:,2)) / 10^6 / 100;
AT = accumarray(floor(RT(:,1) * 10) + 1, RT(:,2)) / 10^6;

% Failure flags
RJF = RJ(:,1);
count_0 = sum(RJF == 0);
count_1 = sum(RJF == 1);
RJFP = [ count_0,  count_1 ];

% Request times
RJT = RJ(:,2);

set(gcf,'PaperUnits','inches','PaperSize',[15,5],'PaperPosition',[0 0 15 5]);

subplot(2, 4, 1:4);
hold on;
bar(AP, 'facecolor', [0.75,0.75,0.75], 'edgecolor', 'none');
bar(AT, 'facecolor', [0,0.75,1], 'edgecolor', 'none');
xlabel('Time Intervals (0.1 sec)');
ylabel('MB, MB * 100');
grid();
axis('tic', 'labelxy');

subplot(2, 4, 5:7);
hist(RJT, 'facecolor', [0,0.75,1], 'edgecolor', 'none');
title('Request Distribution');
xlabel('Time (sec)');
grid();

subplot(2, 4, 8);
h = pie(RJFP, { num2str(count_0), '' });
% num2str(count_1)
set(h,'EdgeColor','none')
title('Success / Failure');
colormap ( [ 0.6, 0.9, 0.6;  0.9, 0.6, 0.6; ] );

% print -dpng -r100 file.png
% convert file.png -trim file.png
