RP = csvread('~/tmp/pyconcz2016-net-failures/naive_probe.csv');
RT = csvread('~/tmp/pyconcz2016-net-failures/naive_download.csv');

% MB total per each 0.1 sec interval
AP = accumarray(floor(RP(:,1) * 10) + 1, RP(:,2)) / 10^6;
AT = accumarray(floor(RT(:,1) * 10) + 1, RT(:,2)) / 10^6;

%subplot (2, 1, 1)
hold on;
bar(AP, 'facecolor', [0.75,0.75,0.75], 'edgecolor', 'none');
bar(AT, 'facecolor', [0,0.75,1], 'edgecolor', 'none');
xlabel('Time Intervals (0.1 sec)');
ylabel('MB');
grid();
axis('tic', 'labelxy');
pbaspect([3, 1]);

% print -dpng file.png
% convert file.png -trim file.png
