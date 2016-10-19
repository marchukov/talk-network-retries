RP = csvread('~/tmp/pyconcz2016-net-failures/naive_long_probe.csv');
RT = csvread('~/tmp/pyconcz2016-net-failures/naive_long_download.csv');

RJ = csvread('~/tmp/pyconcz2016-net-failures/naive_get_json.csv');

% MB total per each 0.1 sec interval
AP = accumarray(floor(RP(:,1) * 10) + 1, RP(:,2)) / 10^6;
AT = accumarray(floor(RT(:,1) * 10) + 1, RT(:,2)) / 10^6 * 10000;

% Failure flags
RJF = RJ(:,1);
count_0 = sum(RJF == 0);
count_1 = sum(RJF == 1);
RJFP = [ count_0,  count_1 ];

% Request times
RJT = RJ(:,2);

set(gcf,'PaperUnits','inches','PaperSize',[15,5],'PaperPosition',[0 0 15 5]);

hold on;
bar(AP, 'facecolor', [0.75,0.75,0.75], 'edgecolor', 'none');
bar(AT, 'facecolor', [0.75,0.75,0.75], 'edgecolor', 'none');
xlabel('Time Intervals (0.1 sec)');
ylabel('MB / 1000, MB');
grid();
axis('tic', 'labelxy');




% print -dpng -r100 file.png
% convert file.png -trim file.png
